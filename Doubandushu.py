"""
爬取豆瓣读书的书名、出版社等
"""

import requests
import re

content = requests.get("https://book.douban.com/").text

# pattern = re.compile("<li.*?cover.*?href=\"(.*?)\".*?title=\"(\w+)\".*?author\">(.*?)</div>.*?year\">(.*?)</span>.*?</li>", re.S)
pattern = re.compile('<li.*?cover.*?href="(.*?)"*?title="(.*?)">.*?</li>', re.S)
for result in re.findall(pattern, content):
    url, title = result
    url = re.sub("\s", "", url)
    title = re.sub("\s", "", title)
    print(url, title)