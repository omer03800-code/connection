import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update getPersonalCopy
    old_copy_func = """                    const getPersonalCopy = (cat, title) => {
                        if (cat === 'university') return `Looks like you studied together at ${title}.`;
                        if (cat === 'highschool') return `You both studied at ${title}. Know each other?`;
                        if (cat === 'workplace') return `Looks like you worked together at ${title}.`;
                        if (cat === 'origincity') return `You both grew up in ${title}.`;
                        if (cat === 'armybase' || cat === 'armyrole') return `You both served at ${title}.`;
                        return `We found this connection through your shared experiences at ${title}.`;
                    };"""
                    
    new_copy_func = """                    const getPersonalCopy = (cat, title) => {
                        if (cat === 'university') return `${title} circle detected.`;
                        if (cat === 'highschool') return `Same ${title} orbit?`;
                        if (cat === 'workplace') return `Shared ${title} history.`;
                        if (cat === 'origincity') return `You both grew up in ${title}.`;
                        if (cat === 'armybase' || cat === 'armyrole') return `${title} connection found.`;
                        return `${title} link discovered.`;
                    };"""
    
    if old_copy_func in content:
        content = content.replace(old_copy_func, new_copy_func)

    # 2, 3, 4, 7, 8: Update HTML template and CSS
    # Smaller heading: 28px -> 20px
    # EXPAND button: remove border, font-weight 300
    # No glow (box-shadow none), smaller margin-bottom
    old_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 25px; padding-bottom: 25px; cursor: pointer; display: flex; flex-direction: column;">
                            <div style="position: absolute; top: 10px; right: 10px;">
                                <button type="button" class="circle-dismiss" style="background:transparent; border:none; color:#000; font-size:24px; cursor:pointer; padding:0; line-height:0.8; font-weight:100; opacity:0.6; outline:none;">&times;</button>
                            </div>
                            <div class="circle-title" style="font-size: 28px; margin-bottom: 16px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1.2; padding-right: 30px;">${getPersonalCopy(circle.category, circle.title)}</div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;">
                                <div class="circle-meta" style="font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500;">
                                    ${circle.people.length} people &middot; Friend &middot; Strength 3
                                </div>
                                <div>
                                    <button type="button" class="circle-toggle info-action-btn" style="margin: 0;">[ EXPAND ]</button>
                                </div>
                            </div>
                        </div>"""

    new_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 25px; padding-bottom: 25px; cursor: pointer; display: flex; flex-direction: column;">
                            <div style="position: absolute; top: 16px; right: 16px;">
                                <button type="button" class="circle-dismiss" style="background:transparent; border:none; color:#000; font-size:24px; cursor:pointer; padding:8px; line-height:0.8; font-weight:100; opacity:0.6; outline:none;">&times;</button>
                            </div>
                            <div class="circle-title" style="font-size: 20px; margin-bottom: 16px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1.2; padding-right: 30px;">${getPersonalCopy(circle.category, circle.title)}</div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;">
                                <div class="circle-meta" style="font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500;">
                                    ${circle.people.length} people &middot; Friend &middot; Strength 3
                                </div>
                                <div>
                                    <button type="button" class="circle-toggle info-action-btn" style="margin: 0; font-weight: 300; border: none;">[ EXPAND ]</button>
                                </div>
                            </div>
                        </div>"""

    if old_html in content:
        content = content.replace(old_html, new_html)

    # CSS update for .suggested-circle-card
    old_css_card = """            .suggested-circle-card {
                background: #ffffff;
                border: 1px solid rgba(0,0,0,0.05);
                padding: 0;
                border-radius: 16px;
                color: #000000;
                width: 100%;
                pointer-events: auto;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                transition: height 0.3s ease;
                margin-bottom: 24px;
            }"""

    new_css_card = """            .suggested-circle-card {
                background: #ffffff;
                border: 1px solid rgba(0,0,0,0.05);
                padding: 0;
                border-radius: 16px;
                color: #000000;
                width: 100%;
                pointer-events: auto;
                box-shadow: none;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                transition: height 0.3s ease;
                margin-bottom: 12px;
            }"""

    if old_css_card in content:
        content = content.replace(old_css_card, new_css_card)

    # 6. Fix dismiss (x) button logic
    # In earlier iteration, dismissBtn was attached to `.circle-dismiss`. We need to ensure it's still attached.
    # We replaced `circle-dismiss` with a new button tag so let's verify JS.
    old_dismiss_logic = """                    const dismissBtn = div.querySelector('.circle-dismiss');
                    if (dismissBtn) {
                        dismissBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            window._dismissedRecs = window._dismissedRecs || new Set();
                            circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                            removeMainCard();
                        });
                    }"""
    
    # Let's ensure this block actually exists in the file.
    if old_dismiss_logic not in content:
        # If it doesn't exist, we must add it.
        # Find where headerWrap click is added.
        headerWrap_listener = """                    headerWrap.addEventListener('click', (e) => {
                        toggleFunc();
                    });"""
        
        new_dismiss_logic = headerWrap_listener + "\n\n" + """                    const dismissBtn = div.querySelector('.circle-dismiss');
                    if (dismissBtn) {
                        dismissBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            window._dismissedRecs = window._dismissedRecs || new Set();
                            circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                            removeMainCard();
                        });
                    }"""
        if headerWrap_listener in content:
            content = content.replace(headerWrap_listener, new_dismiss_logic)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Refined final UI.")

if __name__ == '__main__':
    main()
