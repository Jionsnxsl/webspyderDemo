"""
爬取头条街拍图片
这里发送请求后，返回的内容是JS，没有包含我们想要的内容
需要分析Ajax请求，进行爬取;在网页分析中选择监控XHR就可以
看到发送的Ajax请求。
"""
# TODO: 其实可以考虑使用selenium驱动浏览器进行访问，这样就可以不用分析Ajax了。

import json
import os
from hashlib import md5
import requests
from requests.exceptions import RequestException
import re
from urllib.parse import urlencode
from multiprocessing import Pool


def get_page_index(offset):
    data = {
        "offset": offset,
        "format": "json",
        "keyword": "街拍",
        "autoload": "true",
        "count": 20,
        "cur_tab": 3,
        "from": "gallery"
    }
    url = "https://www.toutiao.com/search_content/?" + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引页失败！")
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and "data" in data.keys():
        for item in data.get("data"):
            yield item.get("article_url")


def get_page_detail(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("获取详情页失败！")
        return None


def parse_page_detail(html, url):
    pattern = re.compile("BASE_DATA.galleryInfo.*?title:(.*?),.*?parse\((.*?)\),", re.S)
    result = pattern.search(html)
    if result:
        title = result.group(1)
        data = json.loads(result.group(2))  # 这里第一次解析出来的是字符串类型
        data = json.loads(data)   # 这里解析出来的才是字典类型
        if data and "sub_images" in data.keys():
            images = [item.get("url") for item in data.get("sub_images")]
            for image in images:
                download_image(image)
            return {
                "title": title,
                "url": url,
                "images": images
            }


def download_image(url):
    try:
        print("正在下载：", url)
        response = requests.get(url)
        if response.status_code == 200:
            save_to_file(response.content)
        return None
    except RequestException:
        print("下载图片失败！")
        return None


def save_to_file(content):
    # 利用md5命名文件，防止同名
    file_path = "{0}/{1}.{2}".format(os.getcwd()+"/toutiao/", md5(content).hexdigest(), "jpg")
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(content)


def main(offset):
    html = get_page_index(offset)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            # 保存到文件
            with open(os.getcwd() + "/toutiao/infomation.txt", "a", encoding="utf-8") as f:
                # 将字典转换为字符串，同时防止中文乱码
                f.write(json.dumps(result, ensure_ascii=False)+"\n")


if __name__=="__main__":
    pages = [x*20 for x in range(10)]
    pool = Pool()
    pool.map(main, pages)
