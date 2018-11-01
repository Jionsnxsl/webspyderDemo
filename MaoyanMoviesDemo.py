"""
爬取猫眼电影排名前一百的数据，并保存，使用正则表达式。
这个没有什么特别，发送requests后直接就给你返回了结果，
并且包含了我们想要的内容。
"""

import re
import json
import requests
import multiprocessing
from requests.exceptions import RequestException
import time


def get_one_page(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parase_one_page(html):
    # print(html)

    # '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name">'
    # '<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?</p>.*?releasetime">(.*?)'
    # '</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>'

    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name">'
                         '<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            "index": item[0],
            "img": item[1],
            "title": item[2],
            "star": item[3].strip()[3:],
            "releasetime": item[4].strip()[5:],
            "score": item[5] + item[6]
        }


def write_to_file(item):
    with open("maoyanmovies.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False)+"\n")


def main(offset):
    url = "https://maoyan.com/board/4?offset=" + str(offset)
    html = get_one_page(url)
    result = parase_one_page(html)
    for item in result:
        write_to_file(item)

if __name__ == "__main__":
    # main(0)

    # 多线程爬取速度很快，但是写入时要注意，可能会出现写入冲突。
    # t1 = time.process_time()
    # pool = multiprocessing.Pool()
    # pool.map(main, [i*10 for i in range(10)])
    # t2 = time.process_time()
    #
    # print(t2-t1)

    t1 = time.time()
    for i in range(10):
        main(10 * i)

    t2 = time.time()
    print(t2-t1)