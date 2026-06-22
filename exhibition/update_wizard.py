import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('wizard_content.html', 'r', encoding='utf-8') as f:
    wizard_content = f.read()

# Define the boundaries for the replacement
start_str = '        <div id="form-progress-bar"'
end_str = '        </form>'

start_idx = html.find(start_str)
end_idx = html.find(end_str) + len(end_str)

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + '        <form id="add-form" style="display: flex; flex-direction: column; flex: 1; overflow: hidden; margin: 0;">\n' + wizard_content + '\n        </form>' + html[end_idx:]
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully updated index.html")
else:
    print("Could not find boundaries")
