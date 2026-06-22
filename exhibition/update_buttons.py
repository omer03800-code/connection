import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace button text to include brackets and uppercase
html = re.sub(r'>BACK</button>', '>[ BACK ]</button>', html)
html = re.sub(r'>CONTINUE</button>', '>[ NEXT ]</button>', html)
html = re.sub(r'>Myself</button>', '>[ MYSELF ]</button>', html)
html = re.sub(r'>Someone Else</button>', '>[ SOMEONE ELSE ]</button>', html)
html = re.sub(r'>SKIP</button>', '>[ SKIP ]</button>', html)
html = re.sub(r'>FINISH &amp; VIEW BEAST</button>', '>[ VIEW BEAST ]</button>', html)
html = re.sub(r'>FINISH & VIEW BEAST</button>', '>[ VIEW BEAST ]</button>', html)

# Replace classes btn-apple-secondary and btn-apple-primary with info-action-btn
html = re.sub(r'class="btn-apple-secondary"', 'class="info-action-btn"', html)
html = re.sub(r'class="btn-apple-primary"', 'class="info-action-btn"', html)

# Remove the innerHTML clearing crash
html = html.replace("document.getElementById('live-network-preview').innerHTML = ''; // reset preview", "// reset preview")

# We should make sure the styling of these buttons doesn't have background explicitly set in inline styles if it overrides
html = re.sub(r'style="flex: 1; max-width: 180px;"', 'style="flex: 1; max-width: 180px; margin: 0 10px;"', html) # Add some margin between buttons

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated HTML")
