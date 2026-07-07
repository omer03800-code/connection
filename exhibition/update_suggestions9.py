import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Update the #wizard-step-rec html styling to center things
    html_target = '<div id="wizard-step-rec" class="wizard-step">'
    html_replacement = '<div id="wizard-step-rec" class="wizard-step" style="text-align: center; height: 100%; overflow-y: auto; padding-top: 40px;">'
    if html_target in content:
        content = content.replace(html_target, html_replacement)

    # Step 2: Remove the inline style padding-right: 180px from recommendation-list
    html_target2 = '<div id="recommendation-list" style="padding-right: 180px;"></div>'
    html_replacement2 = '<div id="recommendation-list"></div>'
    if html_target2 in content:
        content = content.replace(html_target2, html_replacement2)

    # Step 3: Update the CSS
    css_start = "/* --- CIRCLES DESIGN V8 (Expandable List) --- */"
    css_end = "/* Inline Customization Panel */"
    
    if css_start in content and css_end in content:
        start_idx = content.find(css_start)
        end_idx = content.find(css_end)
        
        new_css = """/* --- CIRCLES DESIGN V9 (Centered List) --- */
            #recommendation-list {
                display: flex;
                flex-direction: column;
                gap: 32px;
                width: 100%;
                max-width: 550px;
                margin: 0 auto;
                padding-bottom: 80px;
                text-align: left;
            }
            .suggested-circle-card {
                background: #FFF;
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 8px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-shadow: none;
                transition: height 0.3s ease;
            }
            .circle-header-wrap {
                position: relative;
                padding: 32px;
                cursor: pointer;
            }
            .circle-title {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 20px;
                font-weight: 400;
                color: #111;
                margin-bottom: 12px;
                letter-spacing: -0.01em;
            }
            .circle-context-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }
            .circle-subtitle {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 14px;
                color: #555;
            }
            .circle-meta {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 13px;
                color: #888;
            }
            .circle-toggle {
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
            }
            .circle-content {
                display: none;
                padding: 0 32px 32px 32px;
                background: #FFF;
                border-top: 1px solid rgba(0,0,0,0.06);
            }
            .circle-bulk-actions {
                display: flex;
                justify-content: center;
                gap: 40px;
                margin: 24px 0;
            }
            
            /* Native Button Styles */
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
            }
            .btn-circle-action:hover {
                opacity: 0.5;
            }
            .btn-circle-action:disabled {
                opacity: 0.3;
                cursor: default;
            }

            /* Minimal Person Row */
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
            }
            .circle-content .suggested-card:last-child {
                margin-bottom: 0;
            }
            .circle-content .suggested-card-main {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .circle-content .suggested-name {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 15px;
                font-weight: 400;
                color: #111;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            
            .circle-footer {
                display: flex;
                justify-content: center;
                margin-top: 24px;
            }

            """
        content = content[:start_idx] + new_css + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated index.html with centered list view.")

if __name__ == '__main__':
    main()
