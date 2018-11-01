"""
Pyquery使用示例
"""

from pyquery import PyQuery as pq

html = """
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
"""

# doc 就像是jQuery中$符号
doc = pq(html)
# 可以传入JS选择器选择元素
li = doc("li")
for item in li.items():
    # 获取属性值
    print(item.attr("class"))
    # 获取标签的文本内容
    print(item.text())
