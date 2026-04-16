import json
import os
import argparse
import subprocess
from datetime import datetime

def inject_news(title, content, author="系统自动发布"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'news_list.json')
    
    # 1. 读取现有数据
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        if not isinstance(news_data, list):
            news_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        news_data = []
    
    # 2. 插入新新闻
    new_id = len(news_data) + 1 if news_data else 1
    new_article = {
        "id": new_id,
        "title": title,
        "content": content,
        "author": author,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    news_data.insert(0, new_article)
    
    # 3. 写回文件
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    
    print(f"SUCCESS: 新闻已发布 - {title}")
    return True

def git_push(commit_message):
    """执行 Git 推送，失败不阻塞主流程"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # git add
        subprocess.run(
            ["git", "add", "news_list.json"],
            cwd=script_dir, check=True, capture_output=True, text=True, timeout=10
        )
        # git commit
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=script_dir, check=True, capture_output=True, text=True, timeout=10
        )
        # git push
        subprocess.run(
            ["git", "push"],
            cwd=script_dir, check=True, capture_output=True, text=True, timeout=30
        )
        print(f"GIT: 推送成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"GIT: 推送失败 - {e.stderr.strip() if e.stderr else '无输出'}")
        return False
    except subprocess.TimeoutExpired:
        print("GIT: 推送超时")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="新闻自动发布工具")
    parser.add_argument("--title", required=True, help="新闻标题")
    parser.add_argument("--content", required=True, help="新闻正文")
    parser.add_argument("--author", default="系统自动发布", help="作者名称")
    
    args = parser.parse_args()
    
    # 发布新闻
    if inject_news(args.title, args.content, args.author):
        # 尝试 Git 推送（不影响主流程成功状态）
        git_push(f"Auto-publish: {args.title}")