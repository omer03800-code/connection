import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

setup_js_extra = """
        setupAutocomplete('f-prev-work', 'workplace');
        setupAutocomplete('f-youth', 'youth');
"""
if "setupAutocomplete('f-youth', 'youth');" not in html:
    html = html.replace("setupAutocomplete('f-other', 'other');", "setupAutocomplete('f-other', 'other');\n" + setup_js_extra)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
