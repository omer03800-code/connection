import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('currentStep++')
if idx == -1:
    idx = html.find('currentStep += 1')

if idx != -1:
    start = max(0, idx - 500)
    end = idx + 1000
    print(html[start:end])
else:
    print("Not found")

