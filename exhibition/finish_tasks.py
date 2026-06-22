with open('/Users/omerbarak/.gemini/antigravity/brain/ef399673-4424-4f65-9897-d28c4fe5a145/task.md', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('- `[ ]`', '- `[x]`')
with open('/Users/omerbarak/.gemini/antigravity/brain/ef399673-4424-4f65-9897-d28c4fe5a145/task.md', 'w', encoding='utf-8') as f:
    f.write(text)
