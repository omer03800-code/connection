import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the old function
pattern = r'function addNodeToOrganicPreview\(label, value\)\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
html = re.sub(pattern, '', html)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
