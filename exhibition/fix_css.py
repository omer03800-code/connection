import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

css = """
        /* WIZARD FIXES */
        #add-modal ::placeholder {
            color: rgba(245,245,245,0.2);
            font-size: 11px;
            letter-spacing: 1px;
            font-weight: 300;
        }
        .autocomplete-wrapper {
            position: relative;
        }
        .autocomplete-dropdown {
            position: absolute;
            top: 100%;
            left: 0;
            width: 100%;
            max-height: 150px;
            overflow-y: auto;
            background: #F5F5F5;
            color: #0A0A0A;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
            display: none;
            border: 1px solid rgba(0,0,0,0.1);
        }
        body.light-mode .autocomplete-dropdown {
            background: #0A0A0A;
            color: #F5F5F5;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .autocomplete-item {
            padding: 10px 15px;
            font-size: 13px;
            cursor: pointer;
            border-bottom: 1px solid rgba(0,0,0,0.05);
            display: flex;
            justify-content: space-between;
        }
        body.light-mode .autocomplete-item {
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .autocomplete-item:last-child {
            border-bottom: none;
        }
        .autocomplete-item:hover {
            background: rgba(0,0,0,0.05);
        }
        body.light-mode .autocomplete-item:hover {
            background: rgba(255,255,255,0.05);
        }
        .autocomplete-count {
            font-size: 10px;
            opacity: 0.5;
        }
        /* Buttons layout */
        .wizard-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: auto;
            padding-top: 30px;
        }
"""

html = html.replace('/* Modal Styles */', css + '\n        /* Modal Styles */')

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
