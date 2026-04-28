import json
import os
import argparse
from datetime import datetime

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--author", default="系统自动发布")
    args = parser.parse_args()
    inject_news(args.title, args.content, args.author)