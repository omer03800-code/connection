import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('const nodes =')
while idx != -1:
    print(html[idx:idx+150])
    idx = html.find('const nodes =', idx + 10)

