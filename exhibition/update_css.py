import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update button CSS
css_button_old = """.info-action-btn {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 10px;
            color: #E6E6E6;
            opacity: 1;
            cursor: pointer;
            font-size: 12px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            text-align: center;
            padding: 0 16px;
            margin-bottom: 8px;
            width: auto;
            transition: all 0.2s ease;
            outline: none;
            font-weight: 300;
            box-sizing: border-box;
            height: 32px;
            line-height: 30px;
        }
        .info-action-btn:hover { 
            opacity: 1;
            background: white;
            color: black !important;
            border: 1px solid #F5F5F5;
        }"""

css_button_new = """.info-action-btn {
            background: transparent;
            border: none;
            border-radius: 10px;
            color: #E6E6E6;
            cursor: pointer;
            font-size: 12px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            padding: 5px 10px;
            transition: opacity 0.2s ease;
            font-weight: 300;
        }
        .info-action-btn:hover { 
            opacity: 0.7;
            text-decoration: underline;
        }
        /* Active toggle state for Me/Someone Else */
        .info-action-btn.active-toggle {
            font-weight: 500;
            color: white;
            border-bottom: 1px solid white;
            border-radius: 0;
            padding-bottom: 2px;
        }
        body.light-mode .info-action-btn.active-toggle {
            color: black;
            border-bottom: 1px solid black;
        }
        
        .footer-buttons {
            position: absolute;
            bottom: 30px;
            left: 30px;
            right: 30px;
            display: flex;
            justify-content: space-between;
        }
        .chapter-block {
            margin-bottom: 35px; /* Increased from 20/25px for breathing room */
        }
        .wizard-step {
            display: flex;
            flex-direction: column;
            height: 100%; /* For absolute footer positioning */
        }
        .dynamic-stats {
            font-size: 10px;
            color: rgba(245,245,245,0.3); /* Lower contrast */
            margin-top: 5px;
            letter-spacing: 0.5px;
        }
        body.light-mode .dynamic-stats {
            color: rgba(0,0,0,0.3);
        }
        #add-modal-content {
            position: relative; /* Anchor for absolute footer */
            min-height: 550px;
            padding-bottom: 80px !important; /* Make room for footer */
        }"""

html = html.replace(css_button_old, css_button_new)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
