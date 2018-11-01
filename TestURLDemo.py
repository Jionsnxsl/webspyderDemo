"""
这里主要是测试访问的URL，比如发送JSON请求等
"""

# import requests
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
# }
#
# cookies = {
#     "csrftoken": "G9mFmqPnNk7vhvYKElIRI30p8XzHfdhcILt1vafESAhXcCohVOExGlG6LuPS10gm"
# }
# response = requests.post("http://127.0.0.1:8000/poll/test/", data={"k": "aa"})
# print(response.text)

import os

with open(os.getcwd()+"/media/text.txt", "w") as f:
    f.write("aa")