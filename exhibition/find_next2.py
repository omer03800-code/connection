import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('function nextStep')
if idx != -1:
    print(html[idx:idx+1500])
else:
    print("Not found")

