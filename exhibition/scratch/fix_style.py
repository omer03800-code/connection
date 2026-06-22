import re

with open('public/index.html', 'r') as f:
    content = f.read()

# 1. Change selected font weight from 600 to 500
content = content.replace("fontWeight = '600'", "fontWeight = '500'")

# 2. Change color: white to color: #F5F5F5
content = content.replace("color: white;", "color: #F5F5F5;")
content = content.replace("color:white;", "color:#F5F5F5;")
content = content.replace('color="white"', 'color="#F5F5F5"')
content = content.replace("color: #fff;", "color: #F5F5F5;")

# 3. Change rgba(255, 255, 255, X) to rgba(245, 245, 245, X)
content = content.replace("rgba(255, 255, 255", "rgba(245, 245, 245")
content = content.replace("rgba(255,255,255", "rgba(245,245,245")

# 4. Fix the clicking bug in 3D canvas (triggerFocus = true)
content = content.replace("selectNode(strandId, false)", "selectNode(strandId, true)")
content = content.replace("selectNode(endId, false)", "selectNode(endId, true)")

# 5. Fix bubbling on label click
content = content.replace("span.onclick = () => selectNode(nodeId);", "span.onclick = (e) => { e.stopPropagation(); selectNode(nodeId, true); }; span.onpointerdown = (e) => e.stopPropagation();")

with open('public/index.html', 'w') as f:
    f.write(content)

print("Updates applied.")
