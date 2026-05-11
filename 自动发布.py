import json
import os
import argparse
import subprocess
from datetime import datetime

def git_push_sync(title):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        subprocess.run(["git", "add", "news_list.json"], cwd=script_dir, check=True, capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
        subprocess.run(["git", "commit", "-m", f"Auto-publish: {title}"], cwd=script_dir, check=True, capture_output=True, text=True, timeout=10, encoding='utf-8', errors='ignore')
        # 推送前先拉取远程更新，避免冲突
        subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=script_dir, check=True, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='ignore')
        subprocess.run(["git", "push"], cwd=script_dir, check=True, capture_output=True, text=True, timeout=30, encoding='utf-8', errors='ignore')
        print("GIT: 推送成功")
    except Exception as e:
        print(f"GIT: 推送未完成（可手动 git push）- {e}")

def inject_news(title, content, author="系统自动发布"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'news_list.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        if not isinstance(news_data, list):
            news_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        news_data = []
    
    new_article = {
        "id": len(news_data) + 1 if news_data else 1,
        "title": title,
        "content": content,
        "author": author,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    news_data.insert(0, new_article)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"SUCCESS: 新闻《{title}》已成功发布。")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--author", default="系统自动发布")
    args = parser.parse_args()
    
    # 清洗标题：去掉可能的 "标题=" 前缀
    title = args.title
    if title.startswith("标题="):
        title = title[3:]
    elif title.startswith("标题："):
        title = title[3:]
    elif title.startswith("标题:"):
        title = title[3:]
    
    if inject_news(title, args.content, args.author):
        git_push_sync(title)