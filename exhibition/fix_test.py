import re

with open('test_load.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r"console\.log\('Israel sections visible\?',.*?\)[\s;]+", "", js, flags=re.DOTALL)

with open('test_load.js', 'w', encoding='utf-8') as f:
    f.write(js)
