import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('width: 50%; margin-left: 0; /* Half width and left-aligned */', 'width: max-content; margin-left: 0; /* Left-aligned, fit content */')
html = html.replace('padding: 10px 0;', 'padding: 8px 24px;\n                white-space: nowrap;')
html = html.replace('flex: 1; /* Fix balance */', '/* no flex 1 so it fits perfectly */')

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
