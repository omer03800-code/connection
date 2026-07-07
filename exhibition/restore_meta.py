import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HTML template
    old_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 48px; background: #FFFFFF !important; color: #111111 !important; cursor: pointer;">
                            <div style="position: absolute; top: 16px; right: 16px;">
                                <button type="button" class="btn-circle-action circle-dismiss" style="font-size: 20px; font-weight: 300; background: transparent; border: none; cursor: pointer; color: #111; padding: 8px;">&times;</button>
                            </div>
                            <div class="circle-title" style="font-size: 22px; font-weight: 400; color: #111; padding-right: 40px; margin: 0; line-height: 1.4;">${getPersonalCopy(circle.category, circle.title)}</div>
                        </div>"""

    new_html = """                        <div class="circle-header-wrap" style="position: relative; padding: 48px; padding-bottom: 32px; background: #FFFFFF !important; color: #111111 !important; cursor: pointer; display: flex; flex-direction: column;">
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
                        </div>"""

    if old_html in content:
        content = content.replace(old_html, new_html)

    # 2. Update JS Logic
    old_js = """                    const headerWrap = div.querySelector('.circle-header-wrap');
                    const content = div.querySelector('.circle-content');
                    const peopleList = div.querySelector('.circle-people-list');
                    const toggleFunc = () => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            headerWrap.style.paddingBottom = '48px';
                        } else {
                            content.style.display = 'block';
                            headerWrap.style.paddingBottom = '0';
                        }
                    };"""

    new_js = """                    const headerWrap = div.querySelector('.circle-header-wrap');
                    const content = div.querySelector('.circle-content');
                    const peopleList = div.querySelector('.circle-people-list');
                    const toggleBtn = div.querySelector('.circle-toggle');
                    const toggleFunc = () => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            headerWrap.style.paddingBottom = '32px';
                            if (toggleBtn) toggleBtn.innerText = '[ EXPAND ]';
                        } else {
                            content.style.display = 'block';
                            headerWrap.style.paddingBottom = '0';
                            if (toggleBtn) toggleBtn.innerText = '[ CLOSE ]';
                        }
                    };"""

    if old_js in content:
        content = content.replace(old_js, new_js)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Added back missing meta details and EXPAND button to closed card.")

if __name__ == '__main__':
    main()
