import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to replace everything from "if (rec.type === 'circle') {" down to the end of that block.
    # Actually, it's safer to just split by specific known markers or replace the known innerHTML.
    
    # 1. Update getPersonalCopy
    old_copy_func = """                    const getPersonalCopy = (cat) => {
                        if (cat === 'university') return 'Looks like you studied together.';
                        if (cat === 'highschool') return 'Looks like you went to high school together.';
                        if (cat === 'workplace') return 'Looks like you worked together.';
                        if (cat === 'origincity') return 'You both grew up here. Know each other?';
                        if (cat === 'armybase' || cat === 'armyrole') return 'You both served here.';
                        return 'We found this connection through your shared experiences.';
                    };"""
                    
    new_copy_func = """                    const getPersonalCopy = (cat, title) => {
                        if (cat === 'university') return `Looks like you studied together at ${title}.`;
                        if (cat === 'highschool') return `You both studied at ${title}. Know each other?`;
                        if (cat === 'workplace') return `Looks like you worked together at ${title}.`;
                        if (cat === 'origincity') return `You both grew up in ${title}.`;
                        if (cat === 'armybase' || cat === 'armyrole') return `You both served at ${title}.`;
                        return `We found this connection through your shared experiences at ${title}.`;
                    };"""
    
    if old_copy_func in content:
        content = content.replace(old_copy_func, new_copy_func)

    # 2. Rewrite HTML for circle card
    old_html = """                        <div class="circle-header-wrap" style="display: flex; justify-content: space-between; align-items: flex-start; padding: 48px;">
                            <div class="circle-header-text" style="flex: 1; padding-right: 24px;">
                                <div class="circle-title" style="font-size: 24px; font-weight: 400; color: #111; margin-bottom: 6px;">${circle.title}</div>
                                <div class="circle-subtitle" style="font-size: 14px; font-weight: 300; color: #111; margin-bottom: 6px;">${circle.subtitle}</div>
                                <div class="circle-personal-copy" style="font-size: 14px; font-weight: 300; color: #111; margin-bottom: 16px;">${getPersonalCopy(circle.category)}</div>
                                <div class="circle-meta" style="font-size: 11px; font-weight: 300; color: #111; text-transform: uppercase;">${circle.people.length} people &middot; Friend &middot; Strength 3</div>
                            </div>
                            <div class="circle-header-action">
                                <button type="button" class="circle-toggle btn-circle-action" style="font-size: 11px; font-weight: 300; text-transform: uppercase; background: transparent; border: none; cursor: pointer; color: #111;">[ EXPAND ]</button>
                            </div>
                        </div>
                        <div class="circle-content" style="display: none; padding: 0 48px 48px 48px; background: #FFFFFF !important; border: none !important;">
                            <div class="circle-bulk-actions" style="display: flex; gap: 24px; margin-top: 0; margin-bottom: 32px; flex-wrap: wrap;">
                                <button type="button" class="btn-circle-action btn-bulk-connect">[ CONNECT WITH EVERYONE ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-partial">[ I KNOW SOME ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">[ SKIP CIRCLE ]</button>
                            </div>
                            <div class="circle-people-list"></div>
                            <div class="circle-footer" style="margin-top: 32px;">
                                <button type="button" class="btn-circle-action btn-bulk-customize">[ CUSTOMIZE CONNECTIONS ]</button>
                            </div>
                        </div>"""

    new_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 48px; background: #FFFFFF !important; color: #111111 !important; cursor: pointer;">
                            <div style="position: absolute; top: 16px; right: 16px;">
                                <button type="button" class="btn-circle-action circle-dismiss" style="font-size: 20px; font-weight: 300; background: transparent; border: none; cursor: pointer; color: #111; padding: 8px;">&times;</button>
                            </div>
                            <div class="circle-title" style="font-size: 22px; font-weight: 400; color: #111; padding-right: 40px; margin: 0; line-height: 1.4;">${getPersonalCopy(circle.category, circle.title)}</div>
                        </div>
                        <div class="circle-content" style="display: none; padding: 0 48px 48px 48px; background: #FFFFFF !important; border: none !important;">
                            <div class="circle-bulk-actions" style="display: flex; gap: 24px; margin-bottom: 32px;">
                                <button type="button" class="btn-circle-action btn-bulk-connect">[ I KNOW EVERYONE ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-partial">[ I KNOW SOME ]</button>
                            </div>
                            <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                                <button type="button" class="btn-circle-action btn-bulk-customize" style="font-size: 10px;">[ CUSTOMIZE CONNECTIONS ]</button>
                            </div>
                            <div class="circle-people-list" style="display: flex; flex-direction: column; gap: 4px;"></div>
                        </div>"""
    
    if old_html in content:
        content = content.replace(old_html, new_html)

    # 3. Handle dismiss button binding in toggle logic
    # Find:
    #                     headerWrap.addEventListener('click', (e) => {
    #                         toggleFunc();
    #                     });
    # Add dismiss logic:
    dismiss_logic = """                    headerWrap.addEventListener('click', (e) => {
                        toggleFunc();
                    });
                    
                    const dismissBtn = div.querySelector('.circle-dismiss');
                    if (dismissBtn) {
                        dismissBtn.addEventListener('click', (e) => {
                            e.stopPropagation();
                            window._dismissedRecs = window._dismissedRecs || new Set();
                            circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                            removeMainCard();
                        });
                    }"""
    if "headerWrap.addEventListener('click', (e) => {" in content and "circle-dismiss" not in content:
        content = content.replace("""                    headerWrap.addEventListener('click', (e) => {
                        toggleFunc();
                    });""", dismiss_logic)

    # 4. Remove btn-bulk-skip event listener since the button is gone
    skip_listener = """                    div.querySelector('.btn-bulk-skip').addEventListener('click', (e) => {
                        e.stopPropagation();
                        window._dismissedRecs = window._dismissedRecs || new Set();
                        circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                        removeMainCard();
                    });"""
    if skip_listener in content:
        content = content.replace(skip_listener, "")

    # 5. Fix people list HTML template
    old_person_html = """                            <div class="suggested-card-main">
                                <div class="suggested-name" style="font-size: 16px; color: #111;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                            </div>
                            <div class="suggested-card-edit" style="display: none;">"""
                            
    new_person_html = """                            <div class="suggested-card-main" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: #F5F5F5; border-radius: 4px;">
                                <div class="suggested-name" style="font-size: 14px; font-weight: 300; color: #111;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-meta" style="font-size: 13px; font-weight: 300; color: #555;">Friend &middot; 3</div>
                            </div>
                            <div class="suggested-card-edit" style="display: none; padding: 16px; background: #F5F5F5; border-top: 1px solid #EAEAEA;">"""
                            
    if old_person_html in content:
        content = content.replace(old_person_html, new_person_html)

    # 6. Override the global .suggested-circle-card styling to be absolutely certain it isn't black
    old_css_card = """            .suggested-circle-card {
                background: #FFFFFF !important;
                color: #111111 !important;
                border: 1px solid rgba(0,0,0,0.1) !important;
                border-radius: 8px;"""
    new_css_card = """            .suggested-circle-card {
                background-color: #FFFFFF !important;
                color: #111111 !important;
                border: 1px solid rgba(0,0,0,0.1) !important;
                border-radius: 8px;"""
    
    if old_css_card in content:
        content = content.replace(old_css_card, new_css_card)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated final UI.")

if __name__ == '__main__':
    main()
