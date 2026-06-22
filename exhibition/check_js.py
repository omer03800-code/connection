import re
import subprocess

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

script_match = re.search(r'<script type="module">(.*?)</script>', html, re.DOTALL)
if script_match:
    js_code = script_match.group(1)
    with open('temp_script.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    result = subprocess.run(['node', '-c', 'temp_script.js'], capture_output=True, text=True)
    print("Syntax check:", result.stdout)
    if result.stderr:
        print("Syntax errors:", result.stderr)
else:
    print("No script module found.")
