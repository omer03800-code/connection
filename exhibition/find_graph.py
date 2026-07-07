import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('const gData =')
if idx == -1:
    idx = html.find('const graphData =')

if idx != -1:
    end = html.find(';', idx)
    print(html[idx:idx+1500])
else:
    print("Not found")

