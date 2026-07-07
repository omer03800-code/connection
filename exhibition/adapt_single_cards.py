import sys
import re

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the entire else block for single recommendations:
    # From "} else {" 
    # to "recList.appendChild(div);"
    
    # Let's locate the exact old string
    start_str = "                } else {\n                    const p = rec.data.person;\n                    div.className = 'suggested-circle-card';"
    if start_str not in content:
        print("Could not find single rec block.")
        return

    # We know the old HTML inside the else block:
    old_html_pattern = r"""                        <div class="circle-header-wrap" style="padding-bottom:40px;">
                            <div class="circle-overline">We found a connection you may know\.</div>
                            <div class="circle-title" style="margin-bottom:0;">\$\{p\.name\.replace\(/ \(\[\^ \]\*\)\$/, '&nbsp;\$1'\)\}</div>
                        </div>
                        <div class="circle-content" style="display:block; border-top: none;">
                            <div class="circle-divider" style="margin-top:0;"></div>
                            <div class="circle-bulk-actions">
                                <button type="button" class="btn-circle-action btn-connect-sleek" data-id="\$\{p\.id\}">\[ CONNECT \]</button>
                                <button type="button" class="btn-circle-action btn-customize">\[ CUSTOMIZE \]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">\[ DISMISS \]</button>
                            </div>
                            <div class="suggested-card-edit">
                                <div class="edit-field-group">
                                    <div>
                                        <label class="edit-label">Connection Type</label>
                                        <select class="edit-select type-input">
                                            <option value="close_family">Close Family</option>
                                            <option value="family">Family</option>
                                            <option value="friend" selected>Friend</option>
                                            <option value="acquaintance">Acquaintance</option>
                                            <option value="professional">Professional</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="edit-label">Strength \(1-5\)</label>
                                        <div class="edit-slider-wrap">
                                            <input type="range" class="edit-slider strength-input" min="1" max="5" value="3">
                                            <span class="edit-slider-val strength-display">3</span>
                                        </div>
                                    </div>
                                </div>
                                <div style="display:flex; justify-content: flex-end; gap: 16px;">
                                    <button type="button" class="btn-circle-action btn-remove-custom">\[ CANCEL \]</button>
                                    <button type="button" class="btn-circle-action btn-save-custom">\[ SAVE CONNECTION \]</button>
                                </div>
                            </div>
                        </div>"""

    new_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 25px; padding-bottom: 25px; cursor: default; display: flex; flex-direction: column;">
                            <div style="position: absolute; top: 16px; right: 16px;">
                                <button type="button" class="btn-bulk-skip" style="background:transparent; border:none; color:#000; font-size:24px; cursor:pointer; padding:8px; line-height:0.8; font-weight:100; opacity:0.6; outline:none;">&times;</button>
                            </div>
                            <div class="circle-title" style="font-size: 20px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1.2; padding-right: 30px;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                            <div class="circle-subtitle" style="font-size: 13px; font-weight: 400; color: #666; margin-top: 4px; margin-bottom: 16px;">${rec.data.shared_context || 'Looks like you crossed paths here.'}</div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;">
                                <div class="circle-meta" style="font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500;">
                                    Friend &middot; Strength 3
                                </div>
                                <div style="display: flex; gap: 10px; align-items: center;">
                                    <button type="button" class="info-action-btn btn-customize" style="margin: 0; font-size: 10px; font-weight: 300; border: none; opacity: 0.6;">[ CUSTOMIZE ]</button>
                                    <button type="button" class="info-action-btn btn-connect-sleek" data-id="${p.id}" style="margin: 0; font-weight: 300; border: none;">[ CONNECT ]</button>
                                </div>
                            </div>
                        </div>
                        <div class="circle-content" style="display: none; padding: 0 25px 25px 25px;">
                            <div class="suggested-card-edit" style="display: block; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.05);">
                                <div class="edit-field-group">
                                    <div>
                                        <label class="edit-label">Connection Type</label>
                                        <select class="edit-select type-input">
                                            <option value="close_family">Close Family</option>
                                            <option value="family">Family</option>
                                            <option value="friend" selected>Friend</option>
                                            <option value="acquaintance">Acquaintance</option>
                                            <option value="professional">Professional</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="edit-label">Strength (1-5)</label>
                                        <div class="edit-slider-wrap">
                                            <input type="range" class="edit-slider strength-input" min="1" max="5" value="3">
                                            <span class="edit-slider-val strength-display">3</span>
                                        </div>
                                    </div>
                                </div>
                                <div style="display:flex; justify-content: flex-end; gap: 16px;">
                                    <button type="button" class="info-action-btn btn-remove-custom" style="margin: 0; font-size: 10px; font-weight: 300; border: none; opacity: 0.6;">[ CANCEL ]</button>
                                    <button type="button" class="info-action-btn btn-save-custom" style="margin: 0; font-size: 10px; font-weight: 300; border: none;">[ SAVE CONNECTION ]</button>
                                </div>
                            </div>
                        </div>"""

    content = re.sub(old_html_pattern, new_html, content)

    # Now let's fix the toggle JS for customize button
    old_js = """                    div.querySelector('.btn-customize').addEventListener('click', (e) => {
                        editPanel.style.display = 'block';
                    });
                    
                    div.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                        editPanel.style.display = 'none';
                    });"""

    new_js = """                    const contentPanel = div.querySelector('.circle-content');
                    const headerWrap = div.querySelector('.circle-header-wrap');
                    div.querySelector('.btn-customize').addEventListener('click', (e) => {
                        contentPanel.style.display = 'block';
                        headerWrap.style.paddingBottom = '12px';
                    });
                    
                    div.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                        contentPanel.style.display = 'none';
                        headerWrap.style.paddingBottom = '25px';
                    });"""

    if old_js in content:
        content = content.replace(old_js, new_js)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Refined individual recommendation card.")

if __name__ == '__main__':
    main()
