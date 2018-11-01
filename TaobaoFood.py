"""
这里使用selenium爬取淘宝美食的内容
因为淘宝的页面比较复杂，如果采用分析Ajax请求
方式，会很麻烦；直接采用驱动浏览器的话比较方便，
因为浏览器会帮我们渲染请求结果，同时我们也可以
控制浏览器进行点击、跳转等操作。
(这里有问题，总是会报错！不知道原因！)
"""
import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
browser.set_window_size(1400, 900)
wait = WebDriverWait(browser, 10)


def search():
    try:
        # 打开淘宝首页
        browser.get("https://www.taobao.com/")

        # 获取搜索输入框、搜索按钮
        input_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button")))

        # 进行搜索
        input_btn.send_keys("美食")
        search_btn.click()

        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total")))

        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print("正在跳转：", page_number)
    try:
        input_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        # 发送跳转页码，并跳转
        input_btn.clear()
        input_btn.send_keys(page_number)
        submit_btn.click()
        # 等待到当前加载的页码高亮，因为这才意味着当前页面加载完毕
        # 这里不知道为什么分行会出现错误！
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number)))
    except TimeoutError:
        next_page(page_number)


def get_products():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .item .item")))
        html = browser.page_source
        soup = BeautifulSoup(html, "lxml")
        result = soup.select("#mainsrp-itemlist .item .item")
        print(result)
    except TimeoutError:
        get_products()


def main():
    total = search()
    total = int(re.compile("(\d+)").search(total).group(1))
    for i in range(2, total+1):
        next_page(i)


if __name__ == "__main__":
    try:
        main()
    finally:
        browser.quit()
