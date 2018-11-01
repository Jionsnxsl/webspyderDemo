"""
urllib3 的练习本
"""

import urllib3

http = urllib3.PoolManager()

# 发送GET请求
r = http.request("GET", "http://httpbin.org/robots.txt")
print(r.data)

# 发送POST请求
r = http.request("POST", "http://httpbin.org/post",
                 fields={"hello": "world"})
print(r.status)
# print(r.headers)
# print(r.data)

import json
r = http.request("GET", "http://httpbin.org/ip")
print(json.loads(r.data.decode("utf-8")))

r = http.request("GET", "http://httpbin.org/headers",
                 headers={
                     "X-Something": "value"
                 })
print(r.status)


