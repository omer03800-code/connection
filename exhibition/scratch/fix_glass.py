import re

with open('public/index.html', 'r') as f:
    content = f.read()

# Make .panel more glass-like
content = content.replace("background: rgba(0, 0, 0, 0.6);\n            backdrop-filter: blur(15px);\n            -webkit-backdrop-filter: blur(15px);", "background: rgba(0, 0, 0, 0.25);\n            backdrop-filter: blur(25px);\n            -webkit-backdrop-filter: blur(25px);")

# Make .modal more glass-like
# (Because they both had the exact same string, the previous replace actually caught both .panel and .modal if they had the exact same whitespace. Let's do a regex to be safe.)

content = re.sub(r'background:\s*rgba\(0,\s*0,\s*0,\s*0\.6\);\s*backdrop-filter:\s*blur\(15px\);\s*-webkit-backdrop-filter:\s*blur\(15px\);', 'background: rgba(0, 0, 0, 0.25);\n            backdrop-filter: blur(25px);\n            -webkit-backdrop-filter: blur(25px);', content)

# Fix #conn-secondary-card
content = content.replace('background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);', 'background: rgba(0, 0, 0, 0.25); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);')

# Fix #search-dropdown
content = content.replace('background: rgba(0,0,0,0.85); backdrop-filter: blur(15px);', 'background: rgba(0,0,0,0.3); backdrop-filter: blur(25px);')

# Fix #info-menu-dropdown
content = content.replace('background: rgba(0,0,0,0.8); backdrop-filter: blur(15px);', 'background: rgba(0,0,0,0.3); backdrop-filter: blur(25px);')

with open('public/index.html', 'w') as f:
    f.write(content)

print("Glass effects applied.")
