"""
爬取搜狗微信文章搜索的结果
1、需要使用代理池
2、需要使用cookie
3、尝试使用BeautifulSoup、Pyquery
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import json


base_url = "http://weixin.sogou.com/weixin?"

headers = {
    "Cookie": "SUV=00B92B867005AF095B35EEF05637C674; ABTEST=7|1531748604|v1; IPLOC=CN3502; SUID=00AF05704A42910A000000005B4CA0FC; SUID=00AF05705218910A000000005B4CA0FC; weixinIndexVisited=1; sct=1; JSESSIONID=aaacQi647VXkf69v-4Gsw; ppinf=5|1531794215|1533003815|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyMTp4aWUlRTUlQjAlOTElRTclODElQjV8Y3J0OjEwOjE1MzE3OTQyMTV8cmVmbmljazoyMTp4aWUlRTUlQjAlOTElRTclODElQjV8dXNlcmlkOjQ0Om85dDJsdUVSZTByM0hmbk5JR1hhNWZ1allYZ1FAd2VpeGluLnNvaHUuY29tfA; pprdig=BSZaKUkxn2-9awVH_U1JqPzfe3jpjmgFOJeFcTrRby5kqoTpdRy_ZBRCvoE6U-9eRcPGqgbXAdE5mwFV9awzsGv2JbuVNr769ncV21dO5D1iBMUlCaHM8JOu0F8WwIC8_NAT3S5UfhGrDCH4NmnRCEjbz1empdRix6OJD9Cyx6M; sgid=13-36070981-AVtNUyeXj1sMwlj7q0xXS8Q; ppmdig=1531794215000000ec3f8b1e4574fb8528e1fe471a8cd5a8; PHPSESSID=dcbi7me7tq36ccruejd83aiof5; SUIR=07A9037706027619030EF29407A1978B; SNUID=EB44EF9AEAEF9BC2E9365DECEBD6C1E3",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

proxy = None
MAX_COUNT = 5  # 最大请求次数


def get_proxy():
    try:
        # 代理池：ProxyPool-master项目，运行python run.py即可开启代理池
        # 代理ip保存在redis，使用flask在本地5555端口运行了一个接口
        response = requests.get("http://127.0.0.1:5555/random")
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def get_html(url, count=1):
    global proxy
    if count > MAX_COUNT:
        print("try too many count")
        return None
    try:
        if proxy:
            proxies = {
                "http": "http://" + proxy
            }
            print("using proxy:", proxy)
            response = requests.get(url, headers=headers, allow_redirects=False, proxies=proxies)
        else:
            print("not use proxy")
            response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            proxy = get_proxy()
            if proxy:
                return get_html(url)
            else:
                print("get proxy failed")
                return None
        return None
    except RequestException:
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(page, query="风景"):
    data = {
        "query": query,
        "type": 2,
        "page": page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    soup = BeautifulSoup(html, "lxml")
    tags = soup.select(".news-box .news-list .txt-box h3 a")
    for tag in tags:
        yield tag.get("href")


def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return get_detail(url)


def parse_detail(html):
    # soup = BeautifulSoup(html, "lxml")
    # title = soup.select("#activity-name")[0].get_text(strip=True)
    # nickname = soup.select("#js_profile_qrcode > div > strong")[0].get_text(strip=True)
    # wechat_num = soup.select("#js_profile_qrcode > div > p:nth-of-type(3) > span")[0].get_text(strip=True)
    # content = soup.select("#js_content")[0].get_text(strip=True)

    doc = pq(html)
    title = doc("#activity-name").text()
    nickname = doc("#js_profile_qrcode > div > strong").text()
    wechat_num = doc("#js_profile_qrcode > div > p:nth-child(3) > span").text()
    content = doc("#js_content").text()

    return {
        "title": title,
        "nickname": nickname,
        "wechat_num": wechat_num,
        "content": content
    }


def save_to_file(content):
    with open("weixin_article.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False)+"\n")


def main():
    for i in range(1, 101):
        html = get_index(i)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                reslut = parse_detail(article_html)
                save_to_file(reslut)


if __name__ == "__main__":
    main()