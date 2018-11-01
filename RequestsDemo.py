"""
Reqeusts 练习
"""

import requests

r = requests.get("https://pan.baidu.com/"
                 "box-static/disk-theme/theme/dusk/img/main_bg.png")
with open("main.png", "wb") as f:
    f.write(r.content)


# r = requests.get("http://httpbin.org/get")
#
# # 请求参数
# payload = {"key1": "value1", "key2": "value2"}
# r = requests.get("http://httpbin.org/get", params=payload)
# print(r.url)
# # output: http://httpbin.org/get?key1=value1&key2=value2
#
# # 添加请求头(不区分大小写)
# headers = {'content-type': 'application/json'}
# r = requests.get("http://httpbin.org/get", params=payload, headers=headers)
# print(r.url)



# proxies_pool = {"ip1", "ip2", "ip3", "ip4"}
# proxies = {
#     "http": 'http://' + Select(proxies_pool),
#     "https": "https://" + Select(proxies_pool),
# }
# response = requests.get("http://httpbin.org/ip", proxies=proxies)
# print(response.text)
# # output: {"origin":"66.112.216.253"}

# s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get("http://httpbin.org/cookies")
#
# print(r.text)

# r = s.get('http://httpbin.org/cookies', cookies={'from-my': 'browser'})
# print(r.text)
# # '{"cookies": {"from-my": "browser"}}'
#
# r = s.get('http://httpbin.org/cookies')
# print(r.text)
# # '{"cookies": {}}'


s = requests.Session()
s.cookies.set("test", "123432")
r = s.get('http://httpbin.org/cookies')
print(r.text)  # output: {"cookies":{"test":"123432"}}
# s.cookies.clear()
s.cookies.set("test2", "11111")
r = s.get('http://httpbin.org/cookies')
print(r.text)