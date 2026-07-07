import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('const wizardSteps =')
if idx != -1:
    print(html[idx-100:idx+800])
else:
    print("Not found")

