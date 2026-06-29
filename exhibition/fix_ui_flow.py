import re

with open('public/index.html', 'r') as f:
    content = f.read()

# --- 1. Step 4a btnNext flow updates ---
old_btn_next = """                if (step === 9) btnNext.textContent = '[ JOIN THE NETWORK ]';
                else if (step === '4a') btnNext.textContent = '[ FEED IT ]';
                else btnNext.textContent = '[ CONTINUE ]';
                
                btnNext.style.display = 'inline-block';
                btnNext.onclick = () => {
                    if (step === 0) processStep0();
                    else if (step === 4) processStep4();
                    else if (step === '4a') processStep4a();
                    else if (step === 5) goToWizardStep('5a');
                    else if (step === '5a') goToWizardStep('5b');
                    else if (step === '5b') goToWizardStep(6);
                    else if (step === 6) goToWizardStep(7);
                    else if (step === 7) processStep6();
                    else if (step === 8) {
                        goToWizardStep(9);
                    }
                    else if (step === 9) processStep9();
                };"""
new_btn_next = """                if (step === 8) btnNext.textContent = '[ JOIN THE NETWORK ]';
                else if (step === 9) btnNext.textContent = '[ FEED IT ]';
                else btnNext.textContent = '[ CONTINUE ]';
                
                btnNext.style.display = 'inline-block';
                btnNext.onclick = () => {
                    if (step === 0) processStep0();
                    else if (step === 4) processStep4();
                    else if (step === '4a') goToWizardStep(5);
                    else if (step === 5) goToWizardStep('5a');
                    else if (step === '5a') goToWizardStep('5b');
                    else if (step === '5b') goToWizardStep(6);
                    else if (step === 6) goToWizardStep(7);
                    else if (step === 7) goToWizardStep(9);
                    else if (step === 9) {
                        const hasRecs = generateRecommendations();
                        if (hasRecs) {
                            goToWizardStep(8);
                        } else {
                            processStep9();
                        }
                    }
                    else if (step === 8) processStep9();
                };"""
if old_btn_next in content:
    content = content.replace(old_btn_next, new_btn_next)

# --- 2. Remove black glow (box-shadow) from feed-more-popup-v2 inline style ---
# The inline style in index.html is: box-shadow: 0 4px 15px rgba(255,255,255,0.1);
content = re.sub(r'box-shadow:\s*0\s+4px\s+15px\s+rgba\(255,255,255,0\.1\);', '', content)

# --- 3. Clean up .btn-feed-more CSS ---
old_btn_css = """        .btn-feed-more {
            background: rgba(0, 0, 0, 0.05);
            border: 1px dashed rgba(0,0,0,0.2);
            color: #0a0a0a;"""
new_btn_css = """        .btn-feed-more {
            background: transparent;
            border: none;
            color: #0a0a0a;
            text-decoration: underline;"""
if old_btn_css in content:
    content = content.replace(old_btn_css, new_btn_css)

old_btn_hover = """        .btn-feed-more:hover {
            background: rgba(0,0,0,0.1);
            color: #000;
            border-color: rgba(0,0,0,0.4);
        }
        body.light-mode .btn-feed-more {
            color: #F5F5F5 !important;
            border-color: rgba(255,255,255,0.5) !important;
            background: rgba(255,255,255,0.1) !important;
        }
        body.light-mode .btn-feed-more:hover {
            color: #fff !important;
            border-color: rgba(255,255,255,0.8) !important;
            background: rgba(255,255,255,0.2) !important;
        }"""
new_btn_hover = """        .btn-feed-more:hover {
            background: transparent;
            color: #000;
            opacity: 0.7;
        }
        body.light-mode .btn-feed-more {
            color: #F5F5F5 !important;
            background: transparent !important;
            border: none !important;
        }
        body.light-mode .btn-feed-more:hover {
            color: #fff !important;
            background: transparent !important;
            opacity: 0.7;
        }"""
if old_btn_hover in content:
    content = content.replace(old_btn_hover, new_btn_hover)

# --- 4. Light mode welcome text inversion (Step 10) ---
# Add CSS rule to invert it back in light mode so it remains white
css_to_add = """
        body.light-mode #wizard-step-10 {
            filter: invert(1) hue-rotate(180deg);
        }"""
if "body.light-mode #wizard-step-10" not in content:
    content = content.replace('body.light-mode { filter: invert(1) hue-rotate(180deg); }', 'body.light-mode { filter: invert(1) hue-rotate(180deg); }' + css_to_add)

# --- 5. Popup completeness threshold ---
old_popup_logic = """            if (window._isPartialAdd) {
                const person = people[index];
                const completeness = getPersonCompleteness(person);
                const popupCopy = completeness > 65 ? "Keep feeding to grow their network!" : "There's nothing to discover yet.";
                
                const feedMorePopup = document.createElement('div');
                feedMorePopup.id = 'feed-more-popup-v2';
                
                feedMorePopup.innerHTML = `
                    <div style="font-size: 14px; font-weight: 300; margin-bottom: 15px; opacity: 0.9;">${popupCopy}</div>
                    <button class="btn-feed-more" onclick="window.resumeFeedMore()">[ FEED ME MORE ]</button>
                `;
                labelObjects[index].element.appendChild(feedMorePopup);
            }"""
new_popup_logic = """            if (window._isPartialAdd) {
                const person = people[index];
                const completeness = getPersonCompleteness(person);
                if (completeness < 15) {
                    const popupCopy = "There's nothing to discover yet.";
                    
                    const feedMorePopup = document.createElement('div');
                    feedMorePopup.id = 'feed-more-popup-v2';
                    
                    feedMorePopup.innerHTML = `
                        <div style="font-size: 14px; font-weight: 300; margin-bottom: 15px; opacity: 0.9; text-shadow: none;">${popupCopy}</div>
                        <button class="btn-feed-more" onclick="window.resumeFeedMore()">[ FEED ME MORE ]</button>
                    `;
                    labelObjects[index].element.appendChild(feedMorePopup);
                }
            }"""
if old_popup_logic in content:
    content = content.replace(old_popup_logic, new_popup_logic)


with open('public/index.html', 'w') as f:
    f.write(content)

