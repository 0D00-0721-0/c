import requests
import time
import csv
import re
import os
import signal
import sys
import random
from datetime import datetime

# ==============================
#  全局变量
# ==============================
stop_crawling = False  # 用于 Ctrl+C 中断控制
CHECKPOINT_INTERVAL = 1000  # 每多少条保存一次断点


# ==============================
#  信号处理
# ==============================
def signal_handler(sig, frame):
    """处理 Ctrl+C 信号"""
    global stop_crawling
    print("\n检测到 Ctrl+C，正在安全停止爬取...")
    stop_crawling = True


# ==============================
#  工具函数
# ==============================
def clean_text(text):
    """清理评论内容，去除换行符、emoji 等"""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\u0000-\uFFFF]", "", text)
    return text.strip()


def get_bvid_from_url(url):
    """从B站视频URL中提取 bvid"""
    pattern = r"BV[0-9A-Za-z]{10}"
    match = re.search(pattern, url)
    return match.group(0) if match else None


def get_with_retry(url, params=None, headers=None, cookies=None, retries=3):
    """带重试机制的请求"""
    for attempt in range(retries):
        try:
            response = requests.get(
                url, params=params, headers=headers, cookies=cookies, timeout=10
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"请求失败（第 {attempt+1} 次）：{e}")
            time.sleep(random.uniform(1.5, 3.5))
    return None


# ==============================
#  B站API函数
# ==============================
def get_video_info(bvid):
    """获取视频信息"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.bilibili.com/video/{bvid}",
    }
    response = get_with_retry(url, headers=headers)
    if not response:
        print("获取视频信息失败")
        return None
    data = response.json()
    if data["code"] == 0:
        return data["data"]
    else:
        print(f"视频信息请求失败: {data.get('message', '未知错误')}")
        return None


def get_comments(aid, page=1, session_cookie=None):
    def get_comments(aid, page=1, session_cookie=None):
        "获取指定页数的评论"
    url = "https://api.bilibili.com/x/v2/reply"
    params = {
        "pn": page,
        "type": 1,
        "oid": aid,
        "sort": 1,  # 改为按时间倒序，风控更低
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/av{aid}",
        "Origin": "https://www.bilibili.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
    }

    cookies = {"SESSDATA": session_cookie} if session_cookie else None
    response = get_with_retry(url, params=params, headers=headers, cookies=cookies)
    return response.json() if response else None

# ==============================
#  数据解析函数
# ==============================
def parse_comment(comment):
    """提取单条评论信息"""
    return {
        "comment_id": comment["rpid"],
        "user_id": comment["member"]["mid"],
        "user_name": comment["member"]["uname"],
        "content": clean_text(comment["content"]["message"]),
        "like_count": comment["like"],
        "reply_count": comment["count"],
        "timestamp": comment["ctime"],
        "time": datetime.fromtimestamp(comment["ctime"]).strftime("%Y-%m-%d %H:%M:%S"),
    }


def extract_replies(comment):
    """递归提取楼中楼评论"""
    replies = []
    if "replies" in comment and comment["replies"]:
        for reply in comment["replies"]:
            replies.append(parse_comment(reply))
            replies.extend(extract_replies(reply))
    return replies


# ==============================
#  核心爬取逻辑
# ==============================
def crawl_all_comments(video_url, session_cookie=None, save_path=None, max_pages=None, max_comments=None):
    """爬取指定视频的全部评论"""
    global stop_crawling
    stop_crawling = False
    signal.signal(signal.SIGINT, signal_handler)

    bvid = get_bvid_from_url(video_url)
    if not bvid:
        print("❌ 无法从URL提取BV号")
        return

    video_info = get_video_info(bvid)
    if not video_info:
        print("❌ 获取视频信息失败")
        return

    aid = video_info["aid"]
    title = video_info["title"]
    print(f"\n🎬 开始爬取: {title} (aid={aid}, bvid={bvid})")
    print("按 Ctrl+C 可随时停止")

    # 断点文件路径
    checkpoint_file = f"bilibili_comments_{bvid}_checkpoint.txt"
    start_page = 1

    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, "r") as f:
                start_page = int(f.read().strip())
            print(f"📍 检测到断点文件，从第 {start_page} 页继续爬取")
        except:
            pass

    # 输出文件
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        filename = os.path.join(save_path, f"bilibili_comments_{bvid}.csv")
    else:
        filename = f"bilibili_comments_{bvid}.csv"

    # 初始化 CSV
    is_new_file = not os.path.exists(filename)
    f = open(filename, "a", newline="", encoding="utf-8-sig")
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "comment_id",
            "user_id",
            "user_name",
            "content",
            "like_count",
            "reply_count",
            "timestamp",
            "time",
        ],
    )
    if is_new_file:
        writer.writeheader()

    # 第一页请求
    first_page = get_comments(aid, start_page, session_cookie)
    if not first_page or first_page.get("code") != 0:
        print("❌ 获取第一页评论失败")
        return

    total_comments = first_page["data"]["page"]["count"]
    total_pages = (total_comments + 19) // 20
    print(f"📊 总评论数：{total_comments}，预计页数：{total_pages}")

    if max_pages and max_pages < total_pages:
        total_pages = max_pages
        print(f"⚙️ 应用最大页数限制：{max_pages}")

    # 爬取循环
    page = start_page
    total_saved = 0
    while page <= total_pages and not stop_crawling:
        print(f"📄 正在爬取第 {page}/{total_pages} 页...")
        data = get_comments(aid, page, session_cookie)
        if not data or data["code"] != 0:
            print(f"⚠️ 第 {page} 页爬取失败，跳过")
            page += 1
            continue

        replies = data["data"].get("replies", [])
        if not replies:
            print("🌀 无更多评论")
            break

        page_comments = []
        for comment in replies:
            page_comments.append(parse_comment(comment))
            page_comments.extend(extract_replies(comment))

        writer.writerows(page_comments)
        total_saved += len(page_comments)

        # 保存断点
        if total_saved % CHECKPOINT_INTERVAL < len(page_comments):
            with open(checkpoint_file, "w") as f_ck:
                f_ck.write(str(page))

        print(f"✅ 已保存 {total_saved} 条评论")
        if max_comments and total_saved >= max_comments:
            print(f"🎯 达到最大评论数 {max_comments} 条，停止")
            break

        page += 1
        time.sleep(random.uniform(0.5, 1.5))

    # 收尾
    f.close()
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

    print(f"\n🎉 爬取完成，共保存 {total_saved} 条评论")
    print(f"📁 文件保存到: {os.path.abspath(filename)}")


# ==============================
#  主程序入口
# ==============================
if __name__ == "__main__":
    video_url = "https://www.bilibili.com/video/BV1JQsoz3EtK"  # 示例
    save_path = "results"
    session_cookie = "41c8a2ef%2C1777189115%2C9efbd%2Aa1CjBNQCv6ZvU3UDdyf01GCeTfyytrG_9H3EVu4h6HjxHNOwrGBTZW4ugEqN73VG1gBggSVjY4WFRGb293T1Y4OURpUnJoVkpfQ2F4WUhjcFk3SWxIU080YlB4clhua0tfa1BjWEwtVFRjRnpvVXFHNWdpMGZjS0t0V3d6VUtrWGJ4X1hGeWJOWHRnIIEC"  # 可填入你的 SESSDATA

    crawl_all_comments(
        video_url,
        session_cookie=session_cookie,
        save_path=save_path,
        max_pages=None,
        max_comments=5000,
    )