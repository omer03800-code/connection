import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('async function init()')
if idx != -1:
    end = html.find('// Setup controls', idx)
    print(html[idx+800:idx+2500])
else:
    print("Not found")

