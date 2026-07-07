import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_sig = "if (isCompact) {"
end_sig = "} else {"

start_idx = html.find(start_sig)
end_idx = html.find(end_sig, start_idx)

print(html[start_idx:end_idx])
