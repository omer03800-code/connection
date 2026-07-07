import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('btn-wizard-global-next')
while idx != -1:
    idx2 = html.find('addEventListener', idx)
    if idx2 != -1 and idx2 - idx < 100:
        end = html.find('});', idx2)
        print(html[idx2:end+500])
        break
    idx = html.find('btn-wizard-global-next', idx + 10)

