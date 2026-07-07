import re

with open('/Users/omerbarak/Documents/פגמר/exhibition/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add white-space: nowrap to circle buttons and meta
content = content.replace(
    'class="circle-meta" style="display: flex; align-items: center; gap: 8px; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500; height: 16px;"',
    'class="circle-meta" style="display: flex; align-items: center; gap: 8px; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500; height: 16px; white-space: nowrap;"'
)
content = content.replace(
    '<button type="button" class="circle-toggle info-action-btn" style="margin: 0; font-weight: 300; border: none;">[ EXPAND ]</button>',
    '<button type="button" class="circle-toggle info-action-btn" style="margin: 0; font-weight: 300; border: none; white-space: nowrap;">[ EXPAND ]</button>'
)

# 2. Update the individual card header row and add white-space: nowrap
content = content.replace(
    '<span>Friend &middot; Strength 3</span>',
    '<span class="meta-label">Friend &middot; Strength 3</span>'
)
content = content.replace(
    '<span>Friend &middot; 3</span>',
    '<span class="meta-label">Friend &middot; 3</span>'
)
content = content.replace(
    '<button type="button" class="info-action-btn btn-connect-sleek" data-id="${p.id}" style="margin: 0; font-weight: 300; border: none;">[ CONNECT ]</button>',
    '<button type="button" class="info-action-btn btn-connect-sleek" data-id="${p.id}" style="margin: 0; font-weight: 300; border: none; white-space: nowrap;">[ CONNECT ]</button>'
)
content = content.replace(
    '<button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0.6; padding: 0;">[ EDIT ]</button>',
    '<button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0.6; padding: 0; white-space: nowrap;">[ EDIT ]</button>'
)

# 3. Replace <select> with Custom Dropdown in both places (circle item & individual card)
old_select = """                                        <select class="edit-select type-input">
                                            <option value="close_family">Close Family</option>
                                            <option value="family">Family</option>
                                            <option value="friend" selected>Friend</option>
                                            <option value="acquaintance">Acquaintance</option>
                                            <option value="professional">Professional</option>
                                        </select>"""

new_select = """                                        <div class="custom-select-wrapper" style="position: relative;">
                                            <div class="custom-select-display type-input" data-value="friend" style="border: 1px solid rgba(0,0,0,0.1); padding: 8px 12px; border-radius: 4px; font-size: 11px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: #fff;">
                                                <span class="custom-select-text">Friend</span>
                                                <span style="font-size: 8px; opacity: 0.5;">▼</span>
                                            </div>
                                            <div class="custom-select-dropdown autocomplete-dropdown" style="display: none; background: #ffffff; border: 1px solid rgba(0,0,0,0.1); box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%;">
                                                <div class="autocomplete-item custom-select-item" data-value="close_family" data-label="Close Family" style="color: #111; padding: 8px 12px; font-size: 11px; cursor: pointer; border-bottom: 1px solid rgba(0,0,0,0.05);">Close Family</div>
                                                <div class="autocomplete-item custom-select-item" data-value="family" data-label="Family" style="color: #111; padding: 8px 12px; font-size: 11px; cursor: pointer; border-bottom: 1px solid rgba(0,0,0,0.05);">Family</div>
                                                <div class="autocomplete-item custom-select-item" data-value="friend" data-label="Friend" style="color: #111; padding: 8px 12px; font-size: 11px; cursor: pointer; border-bottom: 1px solid rgba(0,0,0,0.05);">Friend</div>
                                                <div class="autocomplete-item custom-select-item" data-value="acquaintance" data-label="Acquaintance" style="color: #111; padding: 8px 12px; font-size: 11px; cursor: pointer; border-bottom: 1px solid rgba(0,0,0,0.05);">Acquaintance</div>
                                                <div class="autocomplete-item custom-select-item" data-value="professional" data-label="Professional" style="color: #111; padding: 8px 12px; font-size: 11px; cursor: pointer;">Professional</div>
                                            </div>
                                        </div>"""

content = content.replace(old_select, new_select)

# 4. Remove [ CANCEL ] and [ SAVE CONNECTION ] buttons
old_buttons_1 = """                                <div style="display:flex; justify-content: flex-end; gap: 16px;">
                                    <button type="button" class="btn-circle-action btn-remove-custom">[ CANCEL ]</button>
                                    <button type="button" class="btn-circle-action btn-save-custom">[ SAVE CONNECTION ]</button>
                                </div>"""
content = content.replace(old_buttons_1, "")

old_buttons_2 = """                                <div style="display:flex; justify-content: flex-end; gap: 16px;">
                                    <button type="button" class="info-action-btn btn-remove-custom" style="margin: 0; font-size: 10px; font-weight: 300; border: none; opacity: 0.6;">[ CANCEL ]</button>
                                    <button type="button" class="info-action-btn btn-save-custom" style="margin: 0; font-size: 10px; font-weight: 300; border: none;">[ SAVE CONNECTION ]</button>
                                </div>"""
content = content.replace(old_buttons_2, "")

# Remove Javascript listeners for btn-remove-custom from circle items
old_remove_listener_1 = """                        pDiv.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                            editPanel.style.display = 'none';
                        });"""
content = content.replace(old_remove_listener_1, "")

old_remove_listener_2 = """                    div.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                        contentPanel.style.display = 'none';
                        headerWrap.style.paddingBottom = '25px';
                    });"""
content = content.replace(old_remove_listener_2, "")

# 5. Fix JS to handle custom dropdown and live update meta label
# For circle item:
old_circle_js = """                        strengthSlider.addEventListener('input', (e) => {
                            strengthDisplay.innerText = e.target.value;
                        });
                        
                        const editBtn = pDiv.querySelector('.btn-customize-person');"""

new_circle_js = """                        const metaLabel = pDiv.querySelector('.meta-label');
                        const customDisplay = pDiv.querySelector('.custom-select-display');
                        const customDropdown = pDiv.querySelector('.custom-select-dropdown');
                        const customItems = pDiv.querySelectorAll('.custom-select-item');
                        
                        const updateMeta = () => {
                            const typeLabel = customDisplay.querySelector('.custom-select-text').innerText;
                            const strength = strengthSlider.value;
                            if (metaLabel) metaLabel.innerHTML = `${typeLabel} &middot; ${strength}`;
                        };

                        strengthSlider.addEventListener('input', (e) => {
                            strengthDisplay.innerText = e.target.value;
                            updateMeta();
                        });

                        if (customDisplay && customDropdown) {
                            customDisplay.addEventListener('click', (e) => {
                                e.stopPropagation();
                                customDropdown.style.display = customDropdown.style.display === 'none' ? 'block' : 'none';
                            });
                            
                            customItems.forEach(item => {
                                item.addEventListener('click', (e) => {
                                    e.stopPropagation();
                                    const val = item.getAttribute('data-value');
                                    const label = item.getAttribute('data-label');
                                    customDisplay.setAttribute('data-value', val);
                                    customDisplay.querySelector('.custom-select-text').innerText = label;
                                    customDropdown.style.display = 'none';
                                    updateMeta();
                                });
                            });
                            
                            document.addEventListener('click', (e) => {
                                if (!customDisplay.contains(e.target) && !customDropdown.contains(e.target)) {
                                    customDropdown.style.display = 'none';
                                }
                            });
                        }
                        
                        const editBtn = pDiv.querySelector('.btn-customize-person');"""
content = content.replace(old_circle_js, new_circle_js)

# For individual item:
old_indiv_js = """                    strengthSlider.addEventListener('input', (e) => {
                        strengthDisplay.innerText = e.target.value;
                    });
                    
                    div.querySelector('.btn-bulk-skip').addEventListener('click', () => {"""

new_indiv_js = """                    const metaLabel = div.querySelector('.meta-label');
                    const customDisplay = div.querySelector('.custom-select-display');
                    const customDropdown = div.querySelector('.custom-select-dropdown');
                    const customItems = div.querySelectorAll('.custom-select-item');
                    
                    const updateMeta = () => {
                        const typeLabel = customDisplay.querySelector('.custom-select-text').innerText;
                        const strength = strengthSlider.value;
                        if (metaLabel) metaLabel.innerHTML = `${typeLabel} &middot; Strength ${strength}`;
                    };

                    strengthSlider.addEventListener('input', (e) => {
                        strengthDisplay.innerText = e.target.value;
                        updateMeta();
                    });

                    if (customDisplay && customDropdown) {
                        customDisplay.addEventListener('click', (e) => {
                            e.stopPropagation();
                            customDropdown.style.display = customDropdown.style.display === 'none' ? 'block' : 'none';
                        });
                        
                        customItems.forEach(item => {
                            item.addEventListener('click', (e) => {
                                e.stopPropagation();
                                const val = item.getAttribute('data-value');
                                const label = item.getAttribute('data-label');
                                customDisplay.setAttribute('data-value', val);
                                customDisplay.querySelector('.custom-select-text').innerText = label;
                                customDropdown.style.display = 'none';
                                updateMeta();
                            });
                        });
                        
                        document.addEventListener('click', (e) => {
                            if (!customDisplay.contains(e.target) && !customDropdown.contains(e.target)) {
                                customDropdown.style.display = 'none';
                            }
                        });
                    }
                    
                    div.querySelector('.btn-bulk-skip').addEventListener('click', () => {"""
content = content.replace(old_indiv_js, new_indiv_js)


# 6. Read values when clicking [ CONNECT ] or [ ADDED ALL ]
# For circle CONNECT ALL
old_circle_connect = """                                addConnectionEntry(s.person.id, 'friend', 3);"""
new_circle_connect = """                                const typeVal = pCard.querySelector('.type-input').getAttribute('data-value') || 'friend';
                                const strengthVal = parseInt(pCard.querySelector('.strength-input').value, 10) || 3;
                                addConnectionEntry(s.person.id, typeVal, strengthVal);"""
content = content.replace(old_circle_connect, new_circle_connect)

# For individual CONNECT
old_indiv_connect = """                    div.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                        addConnectionEntry(p.id, 'friend', 3);"""
new_indiv_connect = """                    div.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                        const typeVal = div.querySelector('.type-input').getAttribute('data-value') || 'friend';
                        const strengthVal = parseInt(div.querySelector('.strength-input').value, 10) || 3;
                        addConnectionEntry(p.id, typeVal, strengthVal);"""
content = content.replace(old_indiv_connect, new_indiv_connect)

# Save back to file
with open('/Users/omerbarak/Documents/פגמר/exhibition/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied modifications to index.html successfully.")
