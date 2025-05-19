import re
import json
import requests

def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
        return config["session_id"], config["lesson_id"]

def get_urls(session_id, lesson_id):
    headers = {
        "Cookie"     : f"sessionid={session_id}",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    url = f"https://pro.yuketang.cn/api/v3/lesson-summary/replay?lesson_id={lesson_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response = response.json()
        if response['code'] == 0:
            urls = []
            for live in response["data"]["live"]:
                urls.append(live["url"])
            return urls, response["data"]["lesson"]["title"]
    return None, None

def get_video(url):
    headers = {
        "Range"      : "bytes=0-",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    return response


if __name__ == "__main__":

    try:
        session_id, lesson_id = load_config()
    except:
        print("Failed to load config.")
        exit(1)

    urls, title = get_urls(session_id, lesson_id)
    if not urls:
        print("Failed to get video urls.")
        exit(1)
        
    cnt = 0
    filename = re.sub(r'[\\/:*?"<>|]', '.', title)
    for url in urls:
        cnt += 1
        print(f"Downloading video {cnt}/{len(urls)} ...")
        response = get_video(url)
        if response.status_code != 206:
            print(f"Failed to get video {cnt}/{len(urls)}. Status code: {response.status_code}.")
        else:
            with open(f"{filename}_{cnt}.mp4", "wb") as f:
                f.write(response.content)

    print(f"All videos in the lesson {title} have been downloaded.")