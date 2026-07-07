import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('function openEditPersonModal')
end = html.find('function', idx + 10)
if idx != -1:
    print(html[idx:end])
else:
    print("Not found")

