with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('flex-direction: row;', 'flex-direction: column;', 1) # The first one is in #add-modal

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
