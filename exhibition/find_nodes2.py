import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('let nodes =')
while idx != -1:
    print(html[idx:idx+150])
    idx = html.find('let nodes =', idx + 10)

