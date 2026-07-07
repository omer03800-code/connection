import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Move [ DELETE ] button from line 1302 to the bottom of the form
delete_btn_html = """<div style="text-align: center; margin-top: 25px; padding-bottom: 20px;">
                        <button type="button" onclick="deleteEditedPerson()" style="background: transparent; border: none; color: #ff4444; font-size: 11px; font-weight: 500; letter-spacing: 1.5px; cursor: pointer; text-transform: uppercase; text-decoration: underline; opacity: 0.7; transition: 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'">[ DELETE PERSON ]</button>
                    </div>"""

# Remove old delete button wrapper and restore save changes
old_buttons = """                <div style="display: flex; justify-content: center; gap: 15px; margin: 15px 0 20px 0; flex-shrink: 0;">
                    <button type="button" onclick="deleteEditedPerson()" style="background: transparent; border: 1px solid #ff4444; color: #ff4444; font-size: 11px; font-weight: 500; letter-spacing: 1.5px; padding: 12px 25px; border-radius: 30px; cursor: pointer; text-transform: uppercase; transition: 0.2s;" onmouseover="this.style.background='#ff4444'; this.style.color='#fff';" onmouseout="this.style.background='transparent'; this.style.color='#ff4444';">[ DELETE ]</button>
                    <button onclick="saveEditedPerson()" id="btn-edit-save" class="info-action-btn" style="margin: 0; align-self: center;">[ SAVE CHANGES ]</button>
                </div>"""

new_buttons = """                <button onclick="saveEditedPerson()" id="btn-edit-save" class="info-action-btn" style="margin: 15px 0 20px 0; align-self: center; flex-shrink: 0;">[ SAVE CHANGES ]</button>"""

if old_buttons in html:
    html = html.replace(old_buttons, new_buttons)

# Insert delete button before `</div> <!-- End of scroll area -->`
scroll_end_marker = "                </div> <!-- End of scroll area -->"
if scroll_end_marker in html and "[ DELETE PERSON ]" not in html:
    html = html.replace(scroll_end_marker, delete_btn_html + "\n" + scroll_end_marker)

# 2. Rewrite isCompact branch in addConnectionEntry
old_iscompact_inner = """            if (isCompact) {
                div.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1; display: flex; flex-direction: column; position: relative;">
                            <input type="text" class="conn-target" placeholder="Search Name..." value="${defaultName}" autocomplete="off" style="font-family: 'Helvetica', Arial, sans-serif; font-weight: 500; font-size: 15px; border: none; outline: none; background: transparent; color: #111; padding: 0; margin-bottom: 2px; width: 100%; border-bottom: 1px solid rgba(0,0,0,0.05);">
                            <div class="conn-info" style="font-family: 'Helvetica', Arial, sans-serif; font-size: 10px; color: #888;">${infoString}</div>
                            <div class="conn-autocomplete" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 200px; flex-direction: column; max-height: 200px; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;"></div>
                        </div>
                        <button type="button" class="btn-remove-conn" style="background: transparent; border: none; color: #999; cursor: pointer; font-size: 20px; padding: 0 0 0 15px; line-height: 1; transition: 0.2s;">&times;</button>
                    </div>
                    
                    <div style="display: flex; gap: 15px; align-items: center; margin-top: 5px;">
                        <div style="flex: 1; display: flex; flex-direction: column; position: relative;">
                            <div style="font-size: 9px; letter-spacing: 1px; color: #888; text-transform: uppercase; margin-bottom: 4px;">Relationship</div>
                            <div class="conn-type-display" style="font-size: 13px; font-weight: 500; color: #333; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.04); padding: 6px 10px; border-radius: 6px;"><span>${getRelLabel(defaultType)}</span> <span style="font-size: 8px;">▼</span></div>
                            <div class="conn-type-dropdown" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 140px; flex-direction: column; padding: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;">
                                <div class="conn-type-option" data-val="friend" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Friend</div>
                                <div class="conn-type-option" data-val="acquaintance" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Acquaintance</div>
                                <div class="conn-type-option" data-val="family_core" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Close)</div>
                                <div class="conn-type-option" data-val="family_extended" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Ext)</div>
                            </div>
                            <input type="hidden" class="conn-type" value="${defaultType}">
                        </div>
                        
                        <div style="flex: 1; display: flex; flex-direction: column; position: relative;">
                            <div style="font-size: 9px; letter-spacing: 1px; color: #888; text-transform: uppercase; margin-bottom: 4px;">Strength</div>
                            <div style="display: flex; align-items: center; width: 100%; height: 24px; position: relative;">
                                <input type="range" class="conn-strength strength-slider" min="1" max="5" value="${defaultStrength}" style="width: 100%;">
                                <div class="conn-strength-label" style="position: absolute; top: 18px; font-size: 9px; color: #888; transform: translateX(-50%); pointer-events: none;">${defaultStrength}</div>
                            </div>
                        </div>
                    </div>
                `;
            } else {"""

new_iscompact_inner = """            if (isCompact) {
                const isNew = defaultTargetId === null;
                div.innerHTML = `
                    <div class="conn-summary" style="display: ${isNew ? 'none' : 'flex'}; justify-content: space-between; align-items: center; cursor: pointer; padding: 4px 0;">
                        <div class="conn-summary-name" style="font-size: 15px; font-weight: 500; color: #111;">${defaultName || 'New Connection'}</div>
                        <div style="display: flex; gap: 12px; align-items: center; font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; font-weight: 500;">
                            <span class="conn-summary-rel">${getRelLabel(defaultType)}</span>
                            <span class="conn-summary-str">Str <span class="str-val">${defaultStrength}</span></span>
                        </div>
                    </div>
                    
                    <div class="conn-expanded" style="display: ${isNew ? 'block' : 'none'}; border-top: ${isNew ? 'none' : '1px solid rgba(0,0,0,0.06)'}; padding-top: ${isNew ? '0' : '12px'}; margin-top: ${isNew ? '0' : '12px'};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1; display: flex; flex-direction: column; position: relative;">
                                <input type="text" class="conn-target" placeholder="Search Name..." value="${defaultName}" autocomplete="off" style="font-family: 'Helvetica', Arial, sans-serif; font-weight: 500; font-size: 15px; border: none; outline: none; background: transparent; color: #111; padding: 0; margin-bottom: 2px; width: 100%; border-bottom: 1px solid rgba(0,0,0,0.05);">
                                <div class="conn-info" style="font-family: 'Helvetica', Arial, sans-serif; font-size: 10px; color: #888;">${infoString}</div>
                                <div class="conn-autocomplete" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 200px; flex-direction: column; max-height: 200px; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;"></div>
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 15px; align-items: center; margin-top: 15px;">
                            <div style="flex: 1; display: flex; flex-direction: column; position: relative;">
                                <div style="font-size: 9px; letter-spacing: 1px; color: #888; text-transform: uppercase; margin-bottom: 4px;">Relationship</div>
                                <div class="conn-type-display" style="font-size: 13px; font-weight: 500; color: #333; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.04); padding: 6px 10px; border-radius: 6px;"><span>${getRelLabel(defaultType)}</span> <span style="font-size: 8px;">▼</span></div>
                                <div class="conn-type-dropdown" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 140px; flex-direction: column; padding: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;">
                                    <div class="conn-type-option" data-val="friend" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Friend</div>
                                    <div class="conn-type-option" data-val="acquaintance" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Acquaintance</div>
                                    <div class="conn-type-option" data-val="family_core" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Close)</div>
                                    <div class="conn-type-option" data-val="family_extended" style="padding: 10px 12px; font-size: 12px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Ext)</div>
                                </div>
                                <input type="hidden" class="conn-type" value="${defaultType}">
                            </div>
                            
                            <div style="flex: 1; display: flex; flex-direction: column; position: relative;">
                                <div style="font-size: 9px; letter-spacing: 1px; color: #888; text-transform: uppercase; margin-bottom: 4px;">Strength</div>
                                <div style="display: flex; align-items: center; width: 100%; height: 24px; position: relative;">
                                    <input type="range" class="conn-strength strength-slider" min="1" max="5" value="${defaultStrength}" style="width: 100%;">
                                    <div class="conn-strength-label" style="position: absolute; top: 18px; font-size: 9px; color: #888; transform: translateX(-50%); pointer-events: none;">${defaultStrength}</div>
                                </div>
                            </div>
                        </div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
                            <button type="button" class="btn-remove-conn" style="background: transparent; border: none; color: #ff4444; cursor: pointer; font-size: 10px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; padding: 4px 0px; border-radius: 4px; transition: 0.2s;" onmouseover="this.style.opacity='0.7'" onmouseout="this.style.opacity='1'">[ REMOVE ]</button>
                            <button type="button" class="btn-collapse-conn" style="background: #111; border: none; color: #fff; cursor: pointer; font-size: 10px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; padding: 6px 12px; border-radius: 6px; transition: 0.2s;">DONE</button>
                        </div>
                    </div>
                `;
            } else {"""

if old_iscompact_inner in html:
    html = html.replace(old_iscompact_inner, new_iscompact_inner)
else:
    print("Could not find old_iscompact_inner")

# We also need to add the JS event listeners for the toggle
js_events_old = """            // Elements
            const targetInput = div.querySelector('.conn-target');
            const infoDiv = div.querySelector('.conn-info');
            const typeDisplay = div.querySelector('.conn-type-display');"""

js_events_new = """            // Summary Toggle Elements (if compact)
            if (isCompact) {
                const summary = div.querySelector('.conn-summary');
                const expanded = div.querySelector('.conn-expanded');
                if (summary && expanded) {
                    summary.addEventListener('click', () => {
                        summary.style.display = 'none';
                        expanded.style.display = 'block';
                    });
                    div.querySelector('.btn-collapse-conn').addEventListener('click', () => {
                        const nameInput = div.querySelector('.conn-target').value;
                        const relInput = div.querySelector('.conn-type-display span').innerText;
                        const strInput = div.querySelector('.conn-strength').value;
                        
                        div.querySelector('.conn-summary-name').innerText = nameInput || 'New Connection';
                        div.querySelector('.conn-summary-rel').innerText = relInput;
                        div.querySelector('.str-val').innerText = strInput;
                        
                        expanded.style.display = 'none';
                        summary.style.display = 'flex';
                    });
                }
            }

            // Elements
            const targetInput = div.querySelector('.conn-target');
            const infoDiv = div.querySelector('.conn-info');
            const typeDisplay = div.querySelector('.conn-type-display');"""

if js_events_old in html:
    html = html.replace(js_events_old, js_events_new)
else:
    print("Could not find js_events_old")

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated successfully")
