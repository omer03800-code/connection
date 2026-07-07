import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Old HTML injection
    old_html = """                        <div class="circle-header-wrap">
                            <div class="circle-overline">We found a community you may already belong to.</div>
                            <div class="circle-title">${circle.title}</div>
                            <div class="circle-subtitle">${circle.subtitle}</div>
                            <div class="circle-meta">${circle.people.length} suggested connections &middot; Friends, 3</div>
                            <button type="button" class="circle-toggle">EXPAND</button>
                        </div>
                        <div class="circle-content" style="display: block;">
                            <div class="circle-divider"></div>
                            <div class="circle-bulk-actions">
                                <button type="button" class="btn-circle-action btn-bulk-partial">[ I KNOW SOME ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-connect">[ CONNECT WITH EVERYONE ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">[ SKIP CIRCLE ]</button>
                            </div>
                            <div class="circle-people-list"></div>
                            <div class="circle-footer">
                                <button type="button" class="btn-circle-action btn-bulk-customize">[ CUSTOMIZE CONNECTIONS ]</button>
                            </div>
                        </div>"""

    # We need to extract the "personal sentence" logic. 
    # Previously, circle.subtitle contained BOTH the subtitle and the personal sentence, or just one?
    # Actually, let's just make the template clean:
    new_html = """                        <div class="circle-header-wrap">
                            <div class="circle-title" style="font-size: 20px; font-weight: 400; color: #111; margin-bottom: 8px;">${circle.title}</div>
                            <div class="circle-subtitle" style="font-size: 15px; color: #555; margin-bottom: 8px;">${circle.subtitle}</div>
                            <div class="circle-meta" style="font-size: 14px; color: #888; margin-bottom: 8px;">${circle.people.length} people &middot; Friend &middot; Strength 3</div>
                            <button type="button" class="circle-toggle" style="margin-top: 16px;">EXPAND</button>
                        </div>
                        <div class="circle-content" style="display: none; padding-top: 0;">
                            <div class="circle-bulk-actions" style="margin-top: 0; margin-bottom: 24px;">
                                <button type="button" class="btn-circle-action btn-bulk-connect">[ CONNECT WITH EVERYONE ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-partial">[ I KNOW SOME ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">[ SKIP CIRCLE ]</button>
                            </div>
                            <div class="circle-people-list"></div>
                            <div class="circle-footer" style="margin-top: 16px;">
                                <button type="button" class="btn-circle-action btn-bulk-customize">[ CUSTOMIZE ]</button>
                            </div>
                        </div>"""
    
    if old_html in content:
        content = content.replace(old_html, new_html)

    # Now let's fix the inner person cards.
    # The user wants "Just names. No descriptions under every person. No extra labels."
    
    old_person_html = """                            <div class="suggested-card-main">
                                <div class="suggested-name">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-status" style="font-size:11px; color:#888;"></div>
                            </div>
                            <div class="suggested-card-edit">"""
                            
    new_person_html = """                            <div class="suggested-card-main">
                                <div class="suggested-name" style="font-size: 16px; color: #111;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                            </div>
                            <div class="suggested-card-edit" style="display: none;">"""
                            
    if old_person_html in content:
        content = content.replace(old_person_html, new_person_html)

    # Also remove any default `display: block` from suggested-card-edit initially if we added it earlier
    content = content.replace("editors.forEach(ed => ed.style.display = 'block');", "editors.forEach(ed => ed.style.display = 'block');")

    # Let's remove the .circle-overline CSS class entirely if it exists to be safe
    css_overline = """            .circle-overline {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
                color: #888;
                text-transform: uppercase;
                margin-bottom: 12px;
            }"""
    if css_overline in content:
        content = content.replace(css_overline, "")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully simplified the UI.")

if __name__ == '__main__':
    main()
