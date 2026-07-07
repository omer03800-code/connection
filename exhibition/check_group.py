import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('function getGroupForPerson')
if idx != -1:
    end = html.find('}', idx)
    print(html[idx:end+1000])
else:
    print("Not found")

