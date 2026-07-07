import sys
import re

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Update the CSS for .circle-content .suggested-card to force white and override dark mode
    css_to_replace = """            /* Minimal Person Row */
            .circle-content .suggested-card {
                border: 1px solid rgba(0,0,0,0.06);
                background: #FFF;
                border-radius: 6px;
                margin-bottom: 8px;
                padding: 16px 20px;
                display: flex;
                flex-direction: column;
                box-shadow: none;
                animation: none;
                transition: border-color 0.2s;
            }"""
    
    new_css = """            /* Minimal Person Row */
            .circle-content .suggested-card {
                border: 1px solid rgba(0,0,0,0.06) !important;
                background: #FFFFFF !important;
                color: #111111 !important;
                border-radius: 6px !important;
                margin-bottom: 8px !important;
                padding: 16px 20px !important;
                display: flex !important;
                flex-direction: column !important;
                box-shadow: none !important;
                animation: none !important;
                transition: border-color 0.2s;
            }"""
            
    content = content.replace(css_to_replace, new_css)
    
    # Step 2: Remove border-top from .circle-content so it doesn't feel like a separate component
    old_circle_content_css = """            .circle-content {
                display: none;
                padding: 0 32px 32px 32px;
                background: #FFF;
                border-top: 1px solid rgba(0,0,0,0.06);
            }"""
    
    new_circle_content_css = """            .circle-content {
                display: none;
                padding: 0 32px 32px 32px;
                background: #FFFFFF !important;
                border: none !important;
            }"""
            
    content = content.replace(old_circle_content_css, new_circle_content_css)

    # Step 3: Remove pointer-events: none from circle-toggle
    old_toggle_css = """            .circle-toggle {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
                color: #111;
                background: transparent;
                border: none;
                cursor: pointer;
                text-transform: uppercase;
                pointer-events: none;
            }"""
            
    new_toggle_css = """            .circle-toggle {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1px;
                color: #111;
                background: transparent;
                border: none;
                cursor: pointer;
                text-transform: uppercase;
            }"""
    content = content.replace(old_toggle_css, new_toggle_css)

    # Step 4: Fix the JS to remove brackets and arrows, and add click listener to headerWrap
    # JS Replace 1: initial button text
    content = content.replace('<button type="button" class="btn-circle-action circle-toggle">[ CLOSE ] ^</button>',
                              '<button type="button" class="circle-toggle">EXPAND</button>')
                              
    # JS Replace 2: toggleBtn.innerText
    content = content.replace("toggleBtn.innerText = '[ OPEN ] v';", "toggleBtn.innerText = 'EXPAND';")
    content = content.replace("toggleBtn.innerText = '[ CLOSE ] ^';", "toggleBtn.innerText = 'CLOSE';")
    
    # JS Replace 3: Adding headerWrap click listener
    old_listener = """                    toggleBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleFunc();
                    });"""
                    
    new_listener = """                    toggleBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleFunc();
                    });
                    
                    headerWrap.addEventListener('click', (e) => {
                        toggleFunc();
                    });"""
    content = content.replace(old_listener, new_listener)

    # Ensure circle meta has dot instead of HTML entity if needed, but it's fine.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully fixed visual issues.")

if __name__ == '__main__':
    main()
