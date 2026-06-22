import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update modal style to 900px
modal_style = """
        #add-modal {
            width: 90%; max-width: 900px;
            padding: 0;
            flex-direction: row;
        }
        #add-modal .close-btn {
            z-index: 100;
        }
"""
if "#add-modal {" not in html:
    html = html.replace('.modal {', modal_style + '\n        .modal {')

# 2. Update typography and wizard layout styles
new_styles = """        <style>
            .editorial-input {
                background: transparent;
                border: none;
                border-bottom: 1px solid rgba(245,245,245,0.4);
                color: #F5F5F5;
                font-size: 18px; /* Increased */
                padding: 10px 0;
                width: 100%;
                outline: none;
                font-family: inherit;
                transition: border-color 0.3s;
                letter-spacing: 0.5px;
            }
            .editorial-input:focus {
                border-bottom-color: #F5F5F5;
            }
            .editorial-label {
                font-size: 10px; /* Small uppercase */
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: rgba(245,245,245,0.6);
                margin-bottom: 5px;
                display: block;
                font-weight: 500;
            }
            .modal-title {
                font-weight: 200;
                font-size: 32px;
                margin-bottom: 10px;
                color: #F5F5F5;
            }
            .modal-subtitle {
                font-size: 14px;
                color: rgba(245,245,245,0.5);
                margin-bottom: 40px;
            }
            .wizard-layout {
                display: flex; 
                flex-direction: row;
                height: 100%; 
                overflow: hidden;
                width: 100%;
            }
            .wizard-form-area {
                flex: 1.2; 
                padding: 50px; 
                overflow-y: auto; 
                display: flex; 
                flex-direction: column;
            }
            .wizard-preview-area {
                flex: 1; 
                background: rgba(245, 245, 245, 0.02); 
                border-left: 1px solid rgba(245, 245, 245, 0.08); 
                padding: 50px; 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                justify-content: center; /* Center organic network */
                position: relative;
                overflow: hidden;
            }
            /* SVG Network Preview Styles */
            #svg-preview {
                width: 100%;
                height: 100%;
                min-height: 300px;
            }
            .organic-node {
                fill: #F5F5F5;
                filter: drop-shadow(0 0 8px rgba(245,245,245,0.8));
                transition: all 0.5s ease;
            }
            .organic-link {
                fill: none;
                stroke: rgba(245,245,245,0.2);
                stroke-width: 1.5;
                transition: all 0.5s ease;
            }
            .organic-label {
                fill: rgba(245,245,245,0.7);
                font-size: 10px;
                letter-spacing: 1px;
                text-transform: uppercase;
                transition: all 0.5s ease;
            }

            /* Consistent Buttons */
            .btn-apple-primary, .btn-apple-secondary {
                height: 50px;
                border-radius: 12px;
                padding: 0 24px;
                font-size: 14px;
                font-weight: 500;
                letter-spacing: 0.5px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                border: none;
                transition: all 0.2s ease;
            }
            .btn-apple-primary {
                background: #F5F5F5;
                color: #0A0A0A;
                box-shadow: 0 4px 12px rgba(245,245,245,0.15);
            }
            .btn-apple-primary:hover { background: #FFFFFF; transform: scale(1.02); }
            .btn-apple-primary:active { transform: scale(0.98); }
            
            .btn-apple-secondary {
                background: rgba(245,245,245,0.08);
                color: #F5F5F5;
            }
            .btn-apple-secondary:hover { background: rgba(245,245,245,0.15); }
            .btn-apple-secondary:active { background: rgba(245,245,245,0.05); }

            .footer-buttons {
                display: flex; gap: 15px; margin-top: 40px;
            }
            .footer-buttons button {
                flex: 1;
            }
"""

start_idx = html.find('        <style>\n            .editorial-input {')
end_idx = html.find('        </style>', start_idx)
if start_idx != -1 and end_idx != -1:
    old_css = html[start_idx:end_idx]
    # We will replace the block with new_styles
    html = html[:start_idx] + new_styles + html[end_idx:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
