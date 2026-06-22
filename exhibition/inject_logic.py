import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('new_wizard_logic.js', 'r', encoding='utf-8') as f:
    wizard_logic = f.read()

discover_start = html.find('        const discoverModal = document.getElementById(\'discover-modal\');')
discover_end = html.find('        document.getElementById(\'btn-wizard-back-4\').addEventListener(\'click\'')

if discover_start != -1 and discover_end != -1:
    discover_logic = html[discover_start:discover_end]
else:
    discover_logic = ""
    print("Warning: Could not extract discover logic")
    
replace_start = html.find('        function goToWizardStep(step) {')
replace_end = html.find('        function calculateMatchScore(p1, p2) {')

if replace_start != -1 and replace_end != -1:
    new_html = html[:replace_start] + wizard_logic + '\n\n' + discover_logic + '\n\n' + html[replace_end:]
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully injected new wizard logic")
else:
    print("Could not find boundaries for script replacement")
