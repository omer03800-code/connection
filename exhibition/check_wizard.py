import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('id="add-modal"')
end = html.find('</form>', idx)
if idx != -1:
    matches = re.findall(r'id="step-\d+"', html[idx:end])
    print("Steps:", matches)
    
    titles = re.findall(r'<h2>(.*?)</h2>', html[idx:end])
    print("Titles:", titles)
