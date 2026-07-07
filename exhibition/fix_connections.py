import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to find the entire `function addConnectionEntry` and replace its body, or just replace the innerHTML block for isCompact.
marker = "function addConnectionEntry(defaultTargetId = null, defaultType = 'friend', defaultStrength = 3, isCompact = false) {"
start_idx = html.find(marker)
end_idx = html.find("function toggleAdvancedDetails", start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find function")
    exit()

body = html[start_idx:end_idx]

# Let's just use regex to replace everything inside if (isCompact) { div.innerHTML = `...` } else {

pattern = re.compile(r"if \(isCompact\) \{[\s\S]*?\} else \{", re.MULTILINE)
new_content = """if (isCompact) {
                div.style.background = '#fdfdfd';
                div.style.border = '1px solid rgba(0,0,0,0.06)';
                div.style.borderRadius = '8px';
                div.style.padding = '8px 12px';
                div.style.marginBottom = '8px';
                div.style.position = 'relative';
                
                div.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                        <!-- Left side: Name input & Autocomplete -->
                        <div style="flex: 1; min-width: 100px; display: flex; flex-direction: column; position: relative;">
                            <input type="text" class="conn-target" placeholder="Search Name..." value="${defaultName}" autocomplete="off" style="font-family: 'Helvetica', Arial, sans-serif; font-weight: 500; font-size: 14px; border: none; outline: none; background: transparent; color: #111; padding: 0; width: 100%;">
                            <div class="conn-info" style="font-family: 'Helvetica', Arial, sans-serif; font-size: 9px; color: #888; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${infoString}</div>
                            <div class="conn-autocomplete" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 200px; flex-direction: column; max-height: 200px; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;"></div>
                        </div>
                        
                        <!-- Right side: Controls -->
                        <div style="display: flex; gap: 10px; align-items: center; justify-content: flex-end;">
                            <!-- Dropdown -->
                            <div style="position: relative; width: 100px;">
                                <div class="conn-type-display" style="font-size: 11px; font-weight: 500; color: #333; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.04); padding: 6px 8px; border-radius: 6px;"><span>${getRelLabel(defaultType)}</span> <span style="font-size: 7px;">▼</span></div>
                                <div class="conn-type-dropdown" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 120px; flex-direction: column; padding: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;">
                                    <div class="conn-type-option" data-val="friend" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Friend</div>
                                    <div class="conn-type-option" data-val="acquaintance" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Acquaintance</div>
                                    <div class="conn-type-option" data-val="family_core" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Close)</div>
                                    <div class="conn-type-option" data-val="family_extended" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Ext)</div>
                                </div>
                                <input type="hidden" class="conn-type" value="${defaultType}">
                            </div>
                            
                            <!-- Slider -->
                            <div style="display: flex; align-items: center; position: relative; width: 60px;">
                                <input type="range" class="conn-strength strength-slider" min="1" max="5" value="${defaultStrength}" style="width: 100%;">
                            </div>
                            
                            <!-- Remove Button -->
                            <button type="button" class="btn-remove-conn" style="background: transparent; border: none; color: #ff4444; cursor: pointer; font-size: 16px; line-height: 1; padding: 0 0 0 5px; opacity: 0.7; transition: 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'">&times;</button>
                        </div>
                    </div>
                `;
            } else {"""

body_replaced = pattern.sub(new_content, body, count=1)

html = html[:start_idx] + body_replaced + html[end_idx:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated successfully")
