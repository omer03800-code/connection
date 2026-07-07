import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('function buildStructure')
if idx != -1:
    idx_cluster = html.find('cluster', idx)
    if idx_cluster != -1:
        print(html[idx_cluster-500:idx_cluster+1000])
    else:
        print("No cluster found in buildStructure")

