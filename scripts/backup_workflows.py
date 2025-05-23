import psycopg2
import json
import os
import shutil
from urllib.parse import quote_plus
from datetime import datetime
from zipfile import ZipFile

# -------------------------------
# CONFIGURE YOUR POSTGRESQL URL
# -------------------------------

host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

password_encoded = quote_plus(password)
conn_url = f"postgres://{user}:{password_encoded}@{host}:{port}/{db_name}?sslmode=require"

# Paths
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
temp_folder = os.path.join(repo_root, "tmp_n8n_exports")
os.makedirs(temp_folder, exist_ok=True)

# Connect
conn = psycopg2.connect(conn_url)
cur = conn.cursor()

# Fetch all workflows
cur.execute('SELECT id, name, nodes, connections, settings, "versionId" FROM public.workflow_entity;')
workflows = cur.fetchall()

if not workflows:
    print("⚠️ No workflows found.")

# Export each workflow to temp folder
for workflow in workflows:
    id, name, nodes, connections, settings, version_id = workflow
    export_data = {
        "id": str(id),
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "settings": settings or {},
        "versionId": str(version_id)
    }
    safe_name = (name or f"unnamed_{id}").replace(" ", "_").replace("/", "_")
    filepath = os.path.join(temp_folder, f"{safe_name}_{id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)
    print(f"✅ Exported: {filepath}")

# Zip them into root folder
today = datetime.utcnow().strftime("%Y-%m-%d")
zip_filename = os.path.join(repo_root, f"n8n-backup-{today}.zip")

with ZipFile(zip_filename, "w") as zipf:
    for file_name in os.listdir(temp_folder):
        full_path = os.path.join(temp_folder, file_name)
        zipf.write(full_path, arcname=file_name)

print(f"📦 Zipped backup: {zip_filename}")

# Optional: Clean up
shutil.rmtree(temp_folder)
print("🧹 Temp folder cleaned up.")

# Close DB connection
cur.close()
conn.close()
