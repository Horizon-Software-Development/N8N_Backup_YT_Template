# 🔄 n8n Template Auto-Backup to GitHub

This repository sets up a GitHub Action that automatically backs up your **n8n workflows** and **credentials** stored in a PostgreSQL database to GitHub on a weekly basis.

Never lose your workflows again — everything is version-controlled and safely stored.

---

## 🚀 How to Use

1. **Fork this repository**

2. **Add the following secrets to your forked repo** (Settings > Secrets > Actions):

   - `POSTGRES_HOST`
   - `POSTGRES_PORT`
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`

   These should point to your n8n PostgreSQL database.

3. **That’s it!** Backups will run automatically every week via GitHub Actions and commit the latest export to your repo.

---

## 🎥 Need Help Setting It Up?

Here’s a step-by-step walkthrough on YouTube:  
👉 [Watch the tutorial here](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)<- Will update soon! 

---
