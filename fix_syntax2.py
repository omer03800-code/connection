import re
with open('exhibition/public/index.html', 'r') as f:
    text = f.read()

# let's find any occurrences of single quotes followed by comma that might be broken:
matches = re.findall(r"'[^']*\\',", text)
for m in matches:
    print("Found broken string:", m)

