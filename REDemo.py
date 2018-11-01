"""
正则表达式学习
"""

import re

# 基本使用步骤
# 将正则表达式编译成Pattern对象
pattern = re.compile("(\w+) (\w+)(?P<sign>.*)")

# 使用Pattern匹配文本，获得匹配结果，无法匹配时返回None
match = pattern.match("hello world!")

# 返回编号为1和2的子串
print(match.group(1, 2))  # output: ('hello', 'world')

# 以元组形式返回捕获的字符创
print(match.groups())  # output: ('hello', 'world', '!')


# 使用match获得分组结果（默认返回整个匹配的子串）
print(match.group())  # output: hello world!

# 将正则表达式编译成Pattern对象
pattern = re.compile(r'world')

# 使用search()查找匹配的子串，不存在能匹配的子串时将返回None
# 这个例子中使用match()无法成功匹配
match = pattern.search('hello world!')

# 使用Match获得分组信息
print(match.group())  # output: world

p = re.compile('\d+')
print(p.split('one1two2three3four4'))
# output: ['one', 'two', 'three', 'four', '']

p = re.compile('\d+')
print(p.findall('one1two2three3four4'))
# output: ['1', '2', '3', '4']


p = re.compile('\d+')
result = p.sub(" ", 'one1two2three3four4')
print(result)
# output: one two three four

content = "Hello 1234567 world this is Regex Demo"
# 贪婪匹配：匹配尽可能的多的字符
result = re.match("^He.*(\d+).*Demo$", content)
print(result.groups())  # output:("7", )

# 非贪婪匹配：匹配尽可能少的字符
result = re.match("^He.*?(\d+).*Demo$", content)
print(result.groups())  # output:('1234567',)

pattern = re.compile("t")
print(pattern.match("title"))



