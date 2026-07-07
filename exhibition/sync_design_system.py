import sys
import re

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update .suggested-circle-card CSS to match #info-card
    old_css_card = r"""            \.suggested-circle-card \{
                background-color: #FFFFFF !important;
                color: #111111 !important;
                border: 1px solid rgba\(0,0,0,0\.1\) !important;
                border-radius: 8px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-shadow: none;
                transition: height 0\.3s ease;
            \}"""
            
    new_css_card = """            .suggested-circle-card {
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
    
    content = re.sub(old_css_card, new_css_card, content)

    # 2. Add .suggested-circle-card to the light-mode invert list
    old_invert = """        body.light-mode #info-card,
        body.light-mode #conn-secondary-card,
        body.light-mode #edit-person-modal {"""
    
    new_invert = """        body.light-mode #info-card,
        body.light-mode #conn-secondary-card,
        body.light-mode #edit-person-modal,
        body.light-mode .suggested-circle-card {"""
    
    if new_invert not in content:
        content = content.replace(old_invert, new_invert)

    # 3. Update HTML template to use #info-card equivalent internal spacing & typography
    old_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 48px; padding-bottom: 32px; background: #FFFFFF !important; color: #111111 !important; cursor: pointer; display: flex; flex-direction: column;">
                            <div style="position: absolute; top: 16px; right: 16px;">
                                <button type="button" class="btn-circle-action circle-dismiss" style="font-size: 20px; font-weight: 300; background: transparent; border: none; cursor: pointer; color: #111; padding: 8px;">&times;</button>
                            </div>
                            <div class="circle-title" style="font-size: 22px; font-weight: 400; color: #111; padding-right: 40px; margin-bottom: 24px; line-height: 1.4;">${getPersonalCopy(circle.category, circle.title)}</div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                                <div class="circle-meta" style="font-size: 11px; font-weight: 300; color: #555; text-transform: uppercase; letter-spacing: 1px;">
                                    ${circle.people.length} people &middot; Friend &middot; Strength 3
                                </div>
                                <div>
                                    <button type="button" class="circle-toggle btn-circle-action" style="font-size: 11px; font-weight: 300; text-transform: uppercase; color: #111; background: transparent; border: none; padding: 0; cursor: pointer; letter-spacing: 1.5px;">[ EXPAND ]</button>
                                </div>
                            </div>
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

    new_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 25px; padding-bottom: 25px; cursor: pointer; display: flex; flex-direction: column;">
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
                        </div>
                        <div class="circle-content" style="display: none; padding: 0 25px 25px 25px;">
                            <div class="circle-bulk-actions" style="display: flex; gap: 10px; margin-bottom: 25px;">
                                <button type="button" class="info-action-btn btn-bulk-connect" style="margin: 0;">[ I KNOW EVERYONE ]</button>
                                <button type="button" class="info-action-btn btn-bulk-partial" style="margin: 0;">[ I KNOW SOME ]</button>
                            </div>
                            <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                                <button type="button" class="info-action-btn btn-bulk-customize" style="margin: 0; font-size: 10px;">[ CUSTOMIZE CONNECTIONS ]</button>
                            </div>
                            <div class="circle-people-list" style="display: flex; flex-direction: column; gap: 0;"></div>
                        </div>"""

    content = content.replace(old_html, new_html)

    # 4. Update the people list HTML to perfectly match .info-row-v2
    old_person_html = """                            <div class="suggested-card-main" style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: #F5F5F5; border-radius: 4px;">
                                <div class="suggested-name" style="font-size: 14px; font-weight: 300; color: #111;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-meta" style="font-size: 13px; font-weight: 300; color: #555;">Friend &middot; 3</div>
                            </div>"""

    new_person_html = """                            <div class="suggested-card-main info-row-v2" style="margin-bottom: 8px;">
                                <div class="suggested-name" style="font-size: 13px; font-weight: 400; color: #111;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-meta info-row-label" style="text-align: right; color: #666;">Friend &middot; 3</div>
                            </div>"""
                            
    content = content.replace(old_person_html, new_person_html)

    # 5. Fix JS to toggle padding properly
    old_js = """                            headerWrap.style.paddingBottom = '32px';"""
    new_js = """                            headerWrap.style.paddingBottom = '25px';"""
    content = content.replace(old_js, new_js)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated recommendation cards to map 1:1 with info-card component design system.")

if __name__ == '__main__':
    main()
