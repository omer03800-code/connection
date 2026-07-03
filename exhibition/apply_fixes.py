import re

def main():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. tags matched fix is already applied.

    # 2. Exclude current user
    if "const currentName = (document.getElementById('f-name-initial')" not in content:
        target = "let scores = [];\n            people.forEach(p => {"
        replacement = """let scores = [];
            const currentName = (document.getElementById('f-name-initial') ? document.getElementById('f-name-initial').value : '').trim().toLowerCase();
            people.forEach(p => {
                if (currentName && p.name.toLowerCase() === currentName) return;"""
        content = content.replace(target, replacement)

    # 3. Playful messages
    target_msg = '<h3 style="font-weight: 300; margin-top: 30px; letter-spacing: 1px; font-size: 24px;">Looking for existing traces...</h3>'
    replacement_msg = """<h3 id="loading-playful-msg" style="font-weight: 300; margin-top: 30px; letter-spacing: 1px; font-size: 24px;">Looking for existing traces...</h3>"""
    content = content.replace(target_msg, replacement_msg)
    
    target_step10 = "goToWizardStep(10);"
    replacement_step10 = """goToWizardStep(10);
            const playfulMsgs = [
                "Looking for existing traces...",
                "The beast needs more data...",
                "Looks like a ghost... feed me more!",
                "Not enough digital footprint... keep typing!",
                "Searching the matrix...",
                "Connecting the dots... but we need more dots!"
            ];
            const msgEl = document.getElementById('loading-playful-msg');
            if (msgEl) {
                msgEl.textContent = playfulMsgs[Math.floor(Math.random() * playfulMsgs.length)];
            }"""
    content = content.replace(target_step10, replacement_step10)

    # 5. Show step 9 if user skips recommendations
    target_trigger = """const hasRecs = generateRecommendations();
            if (hasRecs) {
                goToWizardStep(recStep);
            } else {
                window._nextWizardStep = nextSessionStep;
                window._isPartialAdd = (nextSessionStep !== null);
                processStep9();
            }"""
    replacement_trigger = """const hasRecs = generateRecommendations();
            if (hasRecs) {
                goToWizardStep(recStep);
            } else {
                goToWizardStep(connStep);
            }"""
    content = content.replace(target_trigger, replacement_trigger)

    # 6. Enable autocomplete
    target_auto = "setupAutocomplete('f-city', 'tw-f-city');"
    replacement_auto = """setupAutocomplete('f-city', 'tw-f-city');
        setupAutocomplete('f-origin-city', 'tw-f-origin-city');
        setupAutocomplete('f-university', 'tw-f-university');
        setupAutocomplete('f-degree', 'tw-f-degree');
        setupAutocomplete('f-army-role', 'tw-f-army-role');
        setupAutocomplete('f-army-base', 'tw-f-army-base');
        setupAutocomplete('f-chapters', 'tw-f-chapters');"""
    content = content.replace(target_auto, replacement_auto)

    # 7. Army tab conditional display (check in conn-3 btnNext)
    # the target is complex so let's do a regex substitution
    target_conn3 = r"else if \(currentStr === 'conn-3'\) \{\s*window\._nextWizardStep = '7';\s*window\._isPartialAdd = true;\s*processStep9\(\);\s*\}"
    replacement_conn3 = """else if (currentStr === 'conn-3') {
                        const cityOrigin = document.getElementById('f-origin-city') ? document.getElementById('f-origin-city').value.toLowerCase() : '';
                        const cityCurrent = document.getElementById('f-city') ? document.getElementById('f-city').value.toLowerCase() : '';
                        const isIsrael = cityOrigin.includes('israel') || cityOrigin.includes('ישראל') || cityCurrent.includes('israel') || cityCurrent.includes('ישראל');
                        window._nextWizardStep = isIsrael ? '7' : '8';
                        window._isPartialAdd = true;
                        processStep9();
                    }"""
    content = re.sub(target_conn3, replacement_conn3, content)

    # 8. Clean up Other chapters
    target_other = """<label>What else defines you?</label>
                    <div class="input-wrapper" id="tw-f-tags">
                        <div class="tags-container" style="padding-right: 40px;">
                            <input type="text" id="f-tags" placeholder="e.g. #Design, #Music..." autocomplete="off">
                            <div class="dropdown-list"></div>
                        </div>
                    </div>"""
    content = content.replace(target_other, "")

    # 9. Back button logic
    target_back = """btnBack.onclick = () => {
                    const currentIndex = stepsWithFooter.indexOf(currentStr);
                    if (currentIndex > 0) goToWizardStep(stepsWithFooter[currentIndex - 1]);
                };"""
    replacement_back = """btnBack.onclick = () => {
                    let backTo = null;
                    if (currentStr === '4') backTo = '0';
                    else if (currentStr === '4a') backTo = '4';
                    else if (currentStr.startsWith('rec-1') || currentStr.startsWith('conn-1')) backTo = '4a';
                    else if (currentStr === '5') backTo = '4a';
                    else if (currentStr.startsWith('rec-2') || currentStr.startsWith('conn-2')) backTo = '5';
                    else if (currentStr === '6') backTo = '5';
                    else if (currentStr.startsWith('rec-3') || currentStr.startsWith('conn-3')) backTo = '6';
                    else if (currentStr === '7') backTo = '6';
                    else if (currentStr.startsWith('rec-4') || currentStr.startsWith('conn-4')) backTo = '7';
                    else if (currentStr === '8') {
                        const cityOrigin = document.getElementById('f-origin-city') ? document.getElementById('f-origin-city').value.toLowerCase() : '';
                        const cityCurrent = document.getElementById('f-city') ? document.getElementById('f-city').value.toLowerCase() : '';
                        const isIsrael = cityOrigin.includes('israel') || cityOrigin.includes('ישראל') || cityCurrent.includes('israel') || cityCurrent.includes('ישראל');
                        backTo = isIsrael ? '7' : '6';
                    }
                    else if (currentStr.startsWith('rec-5') || currentStr.startsWith('conn-5')) backTo = '8';
                    
                    if (backTo) goToWizardStep(backTo);
                };"""
    content = content.replace(target_back, replacement_back)

    # 10. Origin City tags
    target_origin = """<div class="input-wrapper">
                        <input type="text" id="f-origin-city" name="originCity" placeholder="City, Country" autocomplete="off">
                    </div>"""
    replacement_origin = """<div class="input-wrapper" id="tw-f-origin-city">
                        <div class="tags-container">
                            <input type="text" id="f-origin-city" name="originCity" placeholder="City, Country" autocomplete="off">
                            <div class="dropdown-list"></div>
                        </div>
                    </div>"""
    content = content.replace(target_origin, replacement_origin)

    # 11. Student subtext
    target_role = """<input type="text" id="f-role" name="role" placeholder="e.g. Product Designer" autocomplete="off">"""
    replacement_role = target_role + """\n                            <p class="step-explanation" style="margin-top: 5px; font-size: 14px;">If you're a student, you can write 'Student' here.</p>"""
    content = content.replace(target_role, replacement_role)

    # 12. "No, not me" logic
    target_btnno = """document.getElementById('btn-match-no').addEventListener('click', () => {
            document.getElementById('form-mode').value = 'add';
            document.getElementById('form-person-id').value = '';
            goToWizardStep(4);
        });"""
    replacement_btnno = """document.getElementById('btn-match-no').addEventListener('click', () => {
            document.getElementById('form-mode').value = 'add';
            document.getElementById('form-person-id').value = '';
            goToWizardStep('4a');
        });"""
    content = content.replace(target_btnno, replacement_btnno)

    # 13. Disable continue button
    target_btndisplay = "btnNext.style.display = 'inline-block';"
    replacement_btndisplay = """btnNext.style.display = 'inline-block';
                
                // Disable logic
                const inputFieldsMap = {
                    '4a': ['f-origin-city'],
                    '5': ['f-role', 'f-city'],
                    '6': ['f-highschool', 'f-university', 'f-degree'],
                    '7': ['f-army-role', 'f-army-base'],
                    '8': ['f-chapters']
                };
                
                const checkInputs = () => {
                    const fields = inputFieldsMap[currentStr];
                    if (!fields) {
                        btnNext.style.opacity = '1';
                        btnNext.style.pointerEvents = 'auto';
                        return;
                    }
                    
                    let hasValue = false;
                    fields.forEach(fid => {
                        const el = document.getElementById(fid);
                        if (el && el.value.trim().length > 0) hasValue = true;
                        
                        const tw = document.getElementById('tw-' + fid);
                        if (tw && tw.querySelectorAll('.tag-item').length > 0) hasValue = true;
                    });
                    
                    if (hasValue) {
                        btnNext.style.opacity = '1';
                        btnNext.style.pointerEvents = 'auto';
                    } else {
                        btnNext.style.opacity = '0.4';
                        btnNext.style.pointerEvents = 'none';
                    }
                };
                
                checkInputs();
                
                // Attach listeners
                const fields = inputFieldsMap[currentStr] || [];
                fields.forEach(fid => {
                    const el = document.getElementById(fid);
                    if (el) {
                        el.addEventListener('input', checkInputs);
                    }
                    const tw = document.getElementById('tw-' + fid);
                    if (tw) {
                        // MutationObserver for tags
                        const observer = new MutationObserver(checkInputs);
                        observer.observe(tw, { childList: true, subtree: true });
                    }
                });"""
    content = content.replace(target_btndisplay, replacement_btndisplay)

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
