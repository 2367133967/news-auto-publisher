import os
import json
import time
import subprocess

# === 配置部分 ===
# OpenClaw 的日志文件路径（请根据你的用户名修改）
LOG_PATH = os.path.expanduser("~/AppData/Local/Temp/openclaw/openclaw-2026-04-16.log")
# 用于标记已处理过的行，避免重复执行
PROCESSED_MARKER = ".processed_by_watcher"

def process_news(news_data):
    """调用你的自动发布脚本"""
    try:
        title = news_data.get("title", "")
        content = news_data.get("content", "")
        author = news_data.get("author", "系统自动发布")
        
        # 构建命令
        cmd = [
            "python",
            os.path.join(os.path.dirname(__file__), "自动发布.py"),
            "--title", title,
            "--content", content,
            "--author", author
        ]
        
        # 执行脚本
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(f"[Watcher] 已处理新闻: {title}")
        print(f"[Watcher] 脚本输出: {result.stdout.strip()}")
        if result.stderr:
            print(f"[Watcher] 脚本错误: {result.stderr.strip()}")
            
    except Exception as e:
        print(f"[Watcher] 处理新闻时出错: {e}")

def watch_log():
    """监控日志文件"""
    if not os.path.exists(LOG_PATH):
        print(f"[Watcher] 错误：日志文件不存在 - {LOG_PATH}")
        print("[Watcher] 请确保 OpenClaw 已运行并产生过对话。")
        return

    print(f"[Watcher] 开始监控日志: {LOG_PATH}")
    print("[Watcher] 等待 Agent 输出新闻数据...")
    
    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        # 跳到文件末尾，只监控新增内容
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                # 寻找包含特定标记的行，例如 "OPENCLAW_NEWS_JSON:"
                if "OPENCLAW_NEWS_JSON:" in line and PROCESSED_MARKER not in line:
                    try:
                        # 提取 JSON 部分
                        json_str = line.split("OPENCLAW_NEWS_JSON:", 1)[1].strip()
                        news_data = json.loads(json_str)
                        process_news(news_data)
                        # 标记为已处理（可选）
                        # with open(LOG_PATH, 'a') as lf: lf.write(f" {PROCESSED_MARKER}")
                    except Exception as e:
                        print(f"[Watcher] 解析日志行失败: {e}")
            else:
                time.sleep(0.5) # 没有新内容时短暂休眠

if __name__ == "__main__":
    watch_log()