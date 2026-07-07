import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update getPersonalCopy
    old_copy_func = """                    const getPersonalCopy = (cat, title) => {
                        if (cat === 'university') return `${title} circle detected.`;
                        if (cat === 'highschool') return `Same ${title} orbit?`;
                        if (cat === 'workplace') return `Shared ${title} history.`;
                        if (cat === 'origincity') return `You both grew up in ${title}.`;
                        if (cat === 'armybase' || cat === 'armyrole') return `${title} connection found.`;
                        return `${title} link discovered.`;
                    };"""
                    
    new_copy_func = """                    const getPersonalCopy = (cat) => {
                        if (cat === 'university') return `Looks like you studied together.`;
                        if (cat === 'highschool') return `Looks like you studied together.`;
                        if (cat === 'workplace') return `Looks like you worked together.`;
                        if (cat === 'origincity') return `You both grew up here.`;
                        if (cat === 'armybase' || cat === 'armyrole') return `Looks like you served together.`;
                        return `Looks like you crossed paths here.`;
                    };"""
    
    if old_copy_func in content:
        content = content.replace(old_copy_func, new_copy_func)

    # 2. Update HTML template
    old_html = """                            <div class="circle-title" style="font-size: 20px; margin-bottom: 16px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1.2; padding-right: 30px;">${getPersonalCopy(circle.category, circle.title)}</div>"""

    new_html = """                            <div class="circle-title" style="font-size: 20px; font-weight: 500; letter-spacing: 0px; color: #000; line-height: 1.2; padding-right: 30px;">${circle.title}</div>
                            <div class="circle-subtitle" style="font-size: 13px; font-weight: 400; color: #666; margin-top: 4px; margin-bottom: 16px;">${circle.subtitle ? circle.subtitle : getPersonalCopy(circle.category)}</div>"""

    if old_html in content:
        content = content.replace(old_html, new_html)

    # 3. Update spacing (margin-bottom: 12px -> 8px)
    old_css_card = """            .suggested-circle-card {
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
                margin-bottom: 8px;
            }"""

    if old_css_card in content:
        content = content.replace(old_css_card, new_css_card)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Restored Title/Subtitle hierarchy.")

if __name__ == '__main__':
    main()
