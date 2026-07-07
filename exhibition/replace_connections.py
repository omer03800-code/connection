import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the old isCompact section
start_marker = "            if (isCompact) {"
end_marker = "            } else {"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker, start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find isCompact section")
    exit(1)

old_section = html[start_idx:end_idx]

new_section = """            if (isCompact) {
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
"""

html = html.replace(old_section, new_section)

# Remove the old JS toggle logic
toggle_start = "            // Summary Toggle Elements (if compact)"
toggle_end = "            // Name Autocomplete"

t_start_idx = html.find(toggle_start)
t_end_idx = html.find(toggle_end, t_start_idx)

if t_start_idx != -1 and t_end_idx != -1:
    html = html[:t_start_idx] + html[t_end_idx:]

# Also, div padding and direction in isCompact needs to be reset to single line
div_style_start = "            if (isCompact) {\n                div.style.background = '#fdfdfd';"
div_style_end = "            } else {\n                div.style.background = 'transparent';"

ds_idx = html.find(div_style_start)
de_idx = html.find(div_style_end, ds_idx)

if ds_idx != -1 and de_idx != -1:
    old_ds = html[ds_idx:de_idx]
    new_ds = """            if (isCompact) {
                div.style.background = '#fdfdfd';
                div.style.border = '1px solid rgba(0,0,0,0.06)';
                div.style.borderRadius = '8px';
                div.style.padding = '8px 12px';
                div.style.marginBottom = '8px';
                div.style.position = 'relative';
"""
    html = html.replace(old_ds, new_ds)


with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated successfully")
