import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the button from its current location
old_btn_str = '<button onclick="saveEditedPerson()" id="btn-edit-save" class="info-action-btn" style="margin: 15px 0 20px 0; align-self: center; flex-shrink: 0;">[ SAVE CHANGES ]</button>'
if old_btn_str in html:
    html = html.replace(old_btn_str, '')
else:
    print("Could not find the exact button string")

# 2. Insert the button after the connections tab content ends
conn_tab_end_sig = '            </div>\n            \n            <script>'
new_btn_str = '            </div>\n            \n            <button onclick="saveEditedPerson()" id="btn-edit-save" class="info-action-btn" style="margin: 15px 0 20px 0; align-self: center; flex-shrink: 0;">[ SAVE CHANGES ]</button>\n            \n            <script>'

if conn_tab_end_sig in html:
    html = html.replace(conn_tab_end_sig, new_btn_str)
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Moved button successfully")
else:
    print("Could not find insertion point")
