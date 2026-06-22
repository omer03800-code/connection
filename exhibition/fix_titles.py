import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<h2 style="font-weight: 300; margin-bottom: 10px; font-size: 24px;">', '<h2 class="modal-title">')
html = html.replace('<h2 style="font-weight: 300; margin-bottom: 40px; font-size: 28px;">', '<h2 class="modal-title">')
html = html.replace('<h2 style="font-weight: 300; margin-bottom: 10px; font-size: 28px;">', '<h2 class="modal-title">')
html = re.sub(r'<p style="color: rgba\(245,245,245,0\.6\); font-size: 14px; margin-bottom: 30px;">', '<p class="modal-subtitle">', html)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
