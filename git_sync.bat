@echo off
cd /d D:\project1\news-publisher
git add news_list.json
git commit -m "Auto-sync: %date% %time%"
git push