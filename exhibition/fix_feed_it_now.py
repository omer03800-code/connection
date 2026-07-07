import re

with open('/Users/omerbarak/Documents/פגמר/exhibition/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add z-index to btn-summary-feed-now to ensure it is always clickable
old_btn = '<button type="button" id="btn-summary-feed-now" class="info-action-btn" style="margin: 0; color: #fff; border: none;">[ FEED IT NOW ]</button>'
new_btn = '<button type="button" id="btn-summary-feed-now" class="info-action-btn" style="margin: 0; color: #fff; border: none; position: relative; z-index: 1001; cursor: pointer;">[ FEED IT NOW ]</button>'

content = content.replace(old_btn, new_btn)

# 2. Add pointer-events: none to the bottom absolute nav container in summary
old_nav = """                    <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; z-index: 1000; background: transparent;">
                        <button type="button" id="btn-summary-back" class="info-action-btn" style="margin: 0; opacity: 0.8;">[ BACK ]</button>
                        <button type="button" id="btn-summary-continue" class="info-action-btn" style="margin: 0;">[ CONTINUE TO FEED ]</button>
                    </div>"""
new_nav = """                    <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; z-index: 1000; background: transparent; pointer-events: none;">
                        <button type="button" id="btn-summary-back" class="info-action-btn" style="margin: 0; opacity: 0.8; pointer-events: auto;">[ BACK ]</button>
                        <button type="button" id="btn-summary-continue" class="info-action-btn" style="margin: 0; pointer-events: auto;">[ CONTINUE TO FEED ]</button>
                    </div>"""

content = content.replace(old_nav, new_nav)

with open('/Users/omerbarak/Documents/פגמר/exhibition/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied fix_feed_it_now.py")
