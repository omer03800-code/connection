import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update #wizard-step-rec and #recommendation-list alignment
    old_wizard_rec = '<div id="wizard-step-rec" class="wizard-step" style="text-align: center; height: 100%; overflow-y: auto; padding-top: 40px;">'
    new_wizard_rec = '<div id="wizard-step-rec" class="wizard-step" style="text-align: left; height: 100%; overflow-y: auto; padding-top: 40px; display: flex; flex-direction: column; align-items: flex-start;">'
    
    if old_wizard_rec in content:
        content = content.replace(old_wizard_rec, new_wizard_rec)

    # 2. Update headers for wizard-step-rec to be left-aligned and use light typography
    old_h2 = '<h2 style="font-size: 32px; font-weight: 500; letter-spacing: -0.5px; margin-bottom: 8px;">Let\'s find your people.</h2>'
    new_h2 = '<h2 style="font-size: 32px; font-weight: 300; letter-spacing: -0.5px; margin-bottom: 8px;">Let\'s find your people.</h2>'
    content = content.replace(old_h2, new_h2)

    # 3. Update CSS for #recommendation-list and .suggested-circle-card
    old_css_list = """            #recommendation-list {
                display: flex;
                flex-direction: column;
                gap: 32px;
                width: 100%;
                max-width: 550px;
                margin: 0 auto;
                padding-bottom: 80px;
                text-align: left;
            }"""
    new_css_list = """            #recommendation-list {
                display: flex;
                flex-direction: column;
                gap: 32px;
                width: 100%;
                max-width: 600px;
                margin: 0;
                padding-bottom: 80px;
                text-align: left;
            }"""
    content = content.replace(old_css_list, new_css_list)

    # Make .suggested-circle-card have white bg and black text explicitly
    old_css_card = """            .suggested-circle-card {
                background: #FFF;
                border: 1px solid rgba(0,0,0,0.1);"""
    new_css_card = """            .suggested-circle-card {
                background: #FFFFFF !important;
                color: #111111 !important;
                border: 1px solid rgba(0,0,0,0.1) !important;"""
    content = content.replace(old_css_card, new_css_card)

    # 4. Rewrite the innerHTML template in renderSuggestedCircles()
    old_html = """                        <div class="circle-header-wrap">
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

    new_html = """                        <div class="circle-header-wrap" style="display: flex; justify-content: space-between; align-items: flex-start; padding: 48px;">
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
    
    if old_html in content:
        content = content.replace(old_html, new_html)

    # Also update toggle logic to handle brackets
    content = content.replace("toggleBtn.innerText = 'EXPAND';", "toggleBtn.innerText = '[ EXPAND ]';")
    content = content.replace("toggleBtn.innerText = 'CLOSE';", "toggleBtn.innerText = '[ CLOSE ]';")

    # Add getPersonalCopy function if it doesn't exist
    if "function getPersonalCopy(" not in content:
        copy_func = """                if (rec.type === 'circle') {
                    const circle = rec.data;
                    
                    const getPersonalCopy = (cat) => {
                        if (cat === 'university') return 'Looks like you studied together.';
                        if (cat === 'highschool') return 'Looks like you went to high school together.';
                        if (cat === 'workplace') return 'Looks like you worked together.';
                        if (cat === 'origincity') return 'You both grew up here. Know each other?';
                        if (cat === 'armybase' || cat === 'armyrole') return 'You both served here.';
                        return 'We found this connection through your shared experiences.';
                    };"""
        content = content.replace("""                if (rec.type === 'circle') {
                    const circle = rec.data;""", copy_func)

    # Ensure .btn-circle-action CSS has light font-weight
    old_btn_css = """            /* Native Button Styles */
            .btn-circle-action {
                background: transparent;
                border: none;
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 1.5px;
                color: #111;
                cursor: pointer;
                padding: 8px 12px;
                text-transform: uppercase;
                transition: opacity 0.2s;
            }"""
    new_btn_css = """            /* Native Button Styles */
            .btn-circle-action {
                background: transparent !important;
                border: none !important;
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 11px;
                font-weight: 300;
                letter-spacing: 1.5px;
                color: #111 !important;
                cursor: pointer;
                padding: 0;
                text-transform: uppercase;
                transition: opacity 0.2s;
            }
            .btn-circle-action:hover {
                opacity: 0.5;
            }"""
    if old_btn_css in content:
        content = content.replace(old_btn_css, new_btn_css)

    # Also remove padding: 32px from .circle-header-wrap since we inline it now
    old_header_css = """            .circle-header-wrap {
                position: relative;
                padding: 32px;
                cursor: pointer;
            }"""
    new_header_css = """            .circle-header-wrap {
                position: relative;
                cursor: pointer;
            }"""
    if old_header_css in content:
        content = content.replace(old_header_css, new_header_css)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated UI to match exact specs.")

if __name__ == '__main__':
    main()
