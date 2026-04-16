@echo off
cd /d C:\news-publisher
git add news_list.json
git commit -m "Auto-sync: %date% %time%"
git push