import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'>Continue</button>', '>[ NEXT ]</button>', html)
html = re.sub(r'>Back</button>', '>[ BACK ]</button>', html)
html = re.sub(r'>Skip</button>', '>[ SKIP ]</button>', html)
html = re.sub(r'>Finish &amp; View Beast</button>', '>[ VIEW BEAST ]</button>', html)
html = re.sub(r'>Finish & View Beast</button>', '>[ VIEW BEAST ]</button>', html)
html = re.sub(r'>Finish &amp; View BEAST</button>', '>[ VIEW BEAST ]</button>', html)

# Also fix the styling of those buttons so they align correctly
# The info-action-btn doesn't have width:100% by default, so we remove the max-width and let them be inline or flex
html = re.sub(r'style="flex: 1; max-width: 180px; margin: 0 10px;"', 'style="margin: 0 10px;"', html)
html = re.sub(r'style="flex: 1; max-width: 180px;"', 'style="margin: 0 10px;"', html)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
