import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('id="edit-person-overlay"')
end_idx = html.find('<!-- View Person Overlay -->', start_idx)

if start_idx != -1 and end_idx != -1:
    print(html[start_idx:end_idx])
else:
    print("Not found")
