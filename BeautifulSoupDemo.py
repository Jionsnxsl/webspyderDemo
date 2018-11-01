"""
BeautifulSoup使用
"""

from bs4 import BeautifulSoup
import re

html = """
<html><head><title>The Dormouse's story<b>  Apple</b></title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup = BeautifulSoup(html, "lxml")

soup.prettify()
print(soup.title.get_text())
for item in soup.title.strings:
    print(item)
print(soup.p["name"])
print(soup.p.get("name"))
print(soup.select("p a"))
for item in soup.select("p a"):
    print(item)
    print(type(item))
