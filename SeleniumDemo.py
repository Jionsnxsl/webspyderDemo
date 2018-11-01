"""
Selenium使用
"""

from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://www.taobao.com/")


import time

input_btn = browser.find_element_by_id("q")
input_btn.send_keys("iphone")
time.sleep(4)
input_btn.clear()
input_btn.send_keys("ipad")
button = browser.find_element_by_class_name("btn-search")
button.click()

browser.get("https://www.zhihu.com/explore")
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
browser.execute_script("alert('To Buttom')")
