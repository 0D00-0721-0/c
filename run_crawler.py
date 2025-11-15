#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 查找bilibili_comment_crawler.py
    crawler_path = os.path.join(script_dir, "bilibili_comment_crawler.py")
    
    if not os.path.exists(crawler_path):
        print(f"错误: 未找到爬虫脚本 {crawler_path}")
        return
    
    # 使用当前环境的Python解释器运行
    python_exec = sys.executable
    print(f"使用Python解释器: {python_exec}")
    
    try:
        subprocess.run([python_exec, crawler_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"运行爬虫失败: {e}")
    except Exception as e:
        print(f"意外错误: {e}")

if __name__ == "__main__":
    main()
