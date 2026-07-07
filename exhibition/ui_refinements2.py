import re

with open('/Users/omerbarak/Documents/פגמר/exhibition/public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add [ CONNECT ] button next to [ EDIT ]
old_html = """                                    <button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0.6; padding: 0; white-space: nowrap;">[ EDIT ]</button>
                                </div>"""

new_html = """                                    <button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0.6; padding: 0; white-space: nowrap;">[ EDIT ]</button>
                                    <button type="button" class="btn-connect-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; padding: 0; white-space: nowrap;">[ CONNECT ]</button>
                                </div>"""

content = content.replace(old_html, new_html)

# Add event listener for the inline connect button
old_js = """                        const editBtn = pDiv.querySelector('.btn-customize-person');
                        if (editBtn) {
                            editBtn.addEventListener('click', (e) => {
                                e.stopPropagation();
                                editPanel.style.display = editPanel.style.display === 'none' ? 'block' : 'none';
                            });
                        }"""

new_js = """                        const editBtn = pDiv.querySelector('.btn-customize-person');
                        if (editBtn) {
                            editBtn.addEventListener('click', (e) => {
                                e.stopPropagation();
                                editPanel.style.display = editPanel.style.display === 'none' ? 'block' : 'none';
                            });
                        }
                        
                        const connectBtn = pDiv.querySelector('.btn-connect-person');
                        if (connectBtn) {
                            connectBtn.addEventListener('click', (e) => {
                                e.stopPropagation();
                                const typeVal = customDisplay.getAttribute('data-value') || 'friend';
                                const strengthVal = parseInt(strengthSlider.value, 10) || 3;
                                
                                addConnectionEntry(p.id, typeVal, strengthVal);
                                window._addedSomeoneInRecs = true;
                                
                                pDiv.classList.add('is-added');
                                pDiv.style.opacity = '0.5';
                                pDiv.style.borderColor = 'transparent';
                                editPanel.style.display = 'none';
                                connectBtn.innerText = '[ ADDED ]';
                                connectBtn.disabled = true;
                                connectBtn.style.opacity = '0.5';
                            });
                        }"""

content = content.replace(old_js, new_js)

with open('/Users/omerbarak/Documents/פגמר/exhibition/public/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied ui_refinements2.py successfully.")
