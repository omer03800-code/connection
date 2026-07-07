import sys
import re

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove [ CUSTOMIZE CONNECTIONS ] button from circle
    old_customize_btn = r"""                            <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                                <button type="button" class="info-action-btn btn-bulk-customize" style="margin: 0; font-size: 10px;">\[ CUSTOMIZE CONNECTIONS \]</button>
                            </div>"""
    content = re.sub(old_customize_btn, "", content)

    # 2. Modify person row template to include inline [ EDIT ]
    old_person_row = r"""                            <div class="suggested-card-main info-row-v2" style="margin-bottom: 8px;">
                                <div class="suggested-name" style="font-size: 13px; font-weight: 400; color: #111;">\$\{p\.name\.replace\(/ \(\[\^ \]\*\)\$/, '&nbsp;\$1'\)\}</div>
                                <div class="suggested-meta info-row-label" style="text-align: right; color: #666;">Friend &middot; 3</div>
                            </div>"""
                            
    new_person_row = """                            <div class="suggested-card-main info-row-v2" style="margin-bottom: 8px;">
                                <div class="suggested-name" style="font-size: 13px; font-weight: 400; color: #111;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-meta info-row-label" style="display: flex; align-items: center; gap: 8px; color: #666;">
                                    <span>Friend &middot; 3</span>
                                    <button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0.6; padding: 0;">[ EDIT ]</button>
                                </div>
                            </div>"""
    
    content = re.sub(old_person_row, new_person_row, content)

    # 3. Modify circle header to include tags
    old_circle_html = r"""                            <div class="circle-title" style="font-size: 20px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1\.2; padding-right: 30px;">\$\{circle\.title\}</div>
                            <div class="circle-subtitle" style="font-size: 13px; font-weight: 400; color: #666; margin-top: 4px; margin-bottom: 16px;">\$\{circle\.subtitle \? circle\.subtitle : getPersonalCopy\(circle\.category\)\}</div>"""
                            
    new_circle_html = """                            <div class="circle-title" style="font-size: 20px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1.2; padding-right: 30px; margin-bottom: 8px;">${circle.title}</div>
                            <div class="circle-tags" style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 16px;">
                                ${(() => {
                                    if (!circle.subtitle) return `<span class="tag-pill" style="color:#666; border-color:rgba(0,0,0,0.1); background:transparent;">#${getPersonalCopy(circle.category)}</span>`;
                                    const tags = circle.subtitle.split(' · ');
                                    return tags.map(t => `<span class="tag-pill" style="color:#666; border-color:rgba(0,0,0,0.1); background:transparent;">#${t}</span>`).join('');
                                })()}
                            </div>"""

    content = re.sub(old_circle_html, new_circle_html, content)

    # 4. Modify individual card header to include tags and replace [ CUSTOMIZE ] with inline [ EDIT ]
    old_indiv_html = r"""                            <div class="circle-title" style="font-size: 20px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1\.2; padding-right: 30px;">\$\{p\.name\.replace\(/ \(\[\^ \]\*\)\$/, '&nbsp;\$1'\)\}</div>
                            <div class="circle-subtitle" style="font-size: 13px; font-weight: 400; color: #666; margin-top: 4px; margin-bottom: 16px;">\$\{rec\.data\.shared_context \|\| 'Looks like you crossed paths here\.'\}</div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;">
                                <div class="circle-meta" style="font-size: 10px; text-transform: uppercase; letter-spacing: 1\.5px; color: #666; font-weight: 500;">
                                    Friend &middot; Strength 3
                                </div>
                                <div style="display: flex; gap: 10px; align-items: center;">
                                    <button type="button" class="info-action-btn btn-customize" style="margin: 0; font-size: 10px; font-weight: 300; border: none; opacity: 0\.6;">\[ CUSTOMIZE \]</button>
                                    <button type="button" class="info-action-btn btn-connect-sleek" data-id="\$\{p\.id\}" style="margin: 0; font-weight: 300; border: none;">\[ CONNECT \]</button>
                                </div>
                            </div>"""

    new_indiv_html = """                            <div class="circle-title" style="font-size: 20px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1.2; padding-right: 30px; margin-bottom: 8px;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                            <div class="circle-tags" style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 16px;">
                                ${(() => {
                                    if (!rec.data.shared || rec.data.shared.length === 0) return `<span class="tag-pill" style="color:#666; border-color:rgba(0,0,0,0.1); background:transparent;">#Connection</span>`;
                                    return rec.data.shared.map(t => `<span class="tag-pill" style="color:#666; border-color:rgba(0,0,0,0.1); background:transparent;">#${t.split(':')[1] ? t.split(':')[1].split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ') : t}</span>`).join('');
                                })()}
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;">
                                <div class="circle-meta" style="display: flex; align-items: center; gap: 8px; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500;">
                                    <span>Friend &middot; 3</span>
                                    <button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0.6; padding: 0;">[ EDIT ]</button>
                                </div>
                                <div style="display: flex; gap: 10px; align-items: center;">
                                    <button type="button" class="info-action-btn btn-connect-sleek" data-id="${p.id}" style="margin: 0; font-weight: 300; border: none;">[ CONNECT ]</button>
                                </div>
                            </div>"""

    content = re.sub(old_indiv_html, new_indiv_html, content)

    # 5. Add JS event listener for the new btn-customize-person in BOTH places
    
    # In circle logic (around line 6570):
    # pDiv.querySelector('.btn-remove-custom').addEventListener('click', ...)
    old_js_circle_edit = r"""                        pDiv\.querySelector\('\.btn-remove-custom'\)\.addEventListener\('click', \(e\) => \{
                            editPanel\.style\.display = 'none';
                        \}\);"""
                        
    new_js_circle_edit = """                        const editBtn = pDiv.querySelector('.btn-customize-person');
                        if (editBtn) {
                            editBtn.addEventListener('click', (e) => {
                                e.stopPropagation();
                                editPanel.style.display = editPanel.style.display === 'none' ? 'block' : 'none';
                            });
                        }
                        
                        pDiv.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                            editPanel.style.display = 'none';
                        });"""

    content = re.sub(old_js_circle_edit, new_js_circle_edit, content)

    # In individual logic (around line 6665):
    old_js_indiv_edit = r"""                    div\.querySelector\('\.btn-customize'\)\.addEventListener\('click', \(e\) => \{
                        contentPanel\.style\.display = 'block';
                        headerWrap\.style\.paddingBottom = '12px';
                    \}\);"""

    new_js_indiv_edit = """                    div.querySelector('.btn-customize-person').addEventListener('click', (e) => {
                        e.stopPropagation();
                        if (contentPanel.style.display === 'block') {
                            contentPanel.style.display = 'none';
                            headerWrap.style.paddingBottom = '25px';
                        } else {
                            contentPanel.style.display = 'block';
                            headerWrap.style.paddingBottom = '12px';
                        }
                    });"""

    content = re.sub(old_js_indiv_edit, new_js_indiv_edit, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Added tags and inline EDIT buttons.")

if __name__ == '__main__':
    main()
