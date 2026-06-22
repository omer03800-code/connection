import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure any <div class="chapter-block" ...> that contains an autocomplete dropdown has autocomplete-wrapper
def add_wrapper_class(match):
    block = match.group(0)
    if 'autocomplete-dropdown' in block and 'autocomplete-wrapper' not in block:
        return block.replace('class="chapter-block"', 'class="chapter-block autocomplete-wrapper"', 1)
    return block

# Find all chapter-block divs (very simple non-nested regex for this specific structure)
html = re.sub(r'<div class="chapter-block"[^>]*>.*?</div>\s*(?=</div>|<div class="chapter-block"|<div class="footer-buttons")', add_wrapper_class, html, flags=re.DOTALL)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
