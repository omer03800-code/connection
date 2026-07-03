import re

def main():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # STEP 5
    # Remove absolute position from children
    content = re.sub(r'(<div id="wizard-step-5".*?>\s*<h2.*?>.*?</h2>)\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">', 
                     r'\1\n                    <div style="position: absolute; top: 20%; left: 50px; width: calc(100% - 330px); z-index: 20; display: flex; flex-direction: column; gap: 80px;">\n                        <div class="chapter-block autocomplete-wrapper">', content)
    content = re.sub(r'</div>\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">',
                     r'</div>\n\n                        <div class="chapter-block autocomplete-wrapper">', content)
    # Close the flex container at the end of step 5
    content = re.sub(r'(stats-f-workplace"></div>\s*</div>)\s*</div>\s*<!-- STEP 6',
                     r'\1\n                    </div>\n                </div>\n\n                <!-- STEP 6', content)

    # STEP 6
    content = re.sub(r'(<div id="wizard-step-6".*?>\s*<h2.*?>.*?</h2>)\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">', 
                     r'\1\n                    <div style="position: absolute; top: 20%; left: 50px; width: calc(100% - 330px); z-index: 20; display: flex; flex-direction: column; gap: 80px;">\n                        <div class="chapter-block autocomplete-wrapper">', content)
    content = re.sub(r'(stats-f-highschool"></div>\s*</div>)\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">',
                     r'\1\n\n                        <div class="chapter-block autocomplete-wrapper">', content)
    content = re.sub(r'(stats-f-university"></div>\s*</div>)\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">',
                     r'\1\n\n                        <div class="chapter-block autocomplete-wrapper">', content)
    content = re.sub(r'(stats-f-degree"></div>\s*</div>)\s*</div>\s*<!-- STEP 7',
                     r'\1\n                    </div>\n                </div>\n\n                <!-- STEP 7', content)

    # STEP 7
    content = re.sub(r'(<div id="wizard-step-7".*?>\s*<h2.*?>.*?</h2>)\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">', 
                     r'\1\n                    <div style="position: absolute; top: 20%; left: 50px; width: calc(100% - 330px); z-index: 20; display: flex; flex-direction: column; gap: 80px;">\n                        <div class="chapter-block autocomplete-wrapper">', content)
    content = re.sub(r'(stats-f-army-role"></div>\s*</div>)\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">',
                     r'\1\n\n                        <div class="chapter-block autocomplete-wrapper">', content)
    content = re.sub(r'(stats-f-army-base"></div>\s*</div>)\s*</div>\s*<!-- STEP 8',
                     r'\1\n                    </div>\n                </div>\n\n                <!-- STEP 8', content)

    # STEP 8
    content = re.sub(r'(<div id="wizard-step-8".*?>\s*<h2.*?>.*?</h2>)\s*<div class="chapter-block autocomplete-wrapper" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">', 
                     r'\1\n                    <div style="position: absolute; top: 20%; left: 50px; width: calc(100% - 330px); z-index: 20; display: flex; flex-direction: column; gap: 80px;">\n                        <div class="chapter-block autocomplete-wrapper">', content)
    content = re.sub(r'(stats-f-other-value"></div>\s*</div>)\s*<div class="chapter-block" style="position: absolute; top: \d+%; left: \d+px; width: [^;]+; z-index: \d+;">',
                     r'\1\n\n                        <div class="chapter-block">', content)
    content = re.sub(r'(f-tags" name="tags">\s*</div>)\s*</div>\s*<!-- STEP REC',
                     r'\1\n                    </div>\n                </div>\n\n                <!-- STEP REC', content)

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
