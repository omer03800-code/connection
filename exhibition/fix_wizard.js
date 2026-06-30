const fs = require('fs');
const file = 'public/index.html';
let content = fs.readFileSync(file, 'utf8');

// 1. Point 7: Add Work tab hint for students
content = content.replace(
    '<label class="editorial-label">Current Role</label>',
    '<label class="editorial-label">Current Role <span style="font-size: 11px; opacity: 0.6; margin-left: 10px; text-transform: none; letter-spacing: normal;">(If you\'re a student, you can write that instead)</span></label>'
);

// 2. Point 3: Equal and smaller spacing in Education tab
content = content.replace(
    '<div style="position: absolute; top: 20%; left: 50px; width: calc(100% - 330px); z-index: 20; display: flex; flex-direction: column; gap: 80px;">',
    '<div style="position: absolute; top: 20%; left: 50px; width: calc(100% - 330px); z-index: 20; display: flex; flex-direction: column; gap: 40px;">' // There are multiple of these, let's use string replace for wizard-step-6 specifically
);
// Actually, let's do a better replace for step-6:
const step6idx = content.indexOf('id="step-6-title"');
if (step6idx > -1) {
    const gapIdx = content.indexOf('gap: 80px;', step6idx);
    if (gapIdx > -1 && gapIdx < step6idx + 500) {
        content = content.substring(0, gapIdx) + 'gap: 30px;' + content.substring(gapIdx + 10);
    }
}

// 3. Point 6: Make "Originally From" a multi-tag input
const oldOriginHtml = `                        <div class="chapter-block autocomplete-wrapper">
                            <label class="editorial-label">Originally From</label>
                            <input type="text" id="f-origin-city" class="editorial-input" placeholder="Where did you grow up?">
                            <div class="autocomplete-list" id="autocomplete-f-origin-city"></div>
                        </div>`;
const newOriginHtml = `                        <div class="chapter-block autocomplete-wrapper">
                            <label class="editorial-label">Originally From</label>
                            <div class="tags-wrapper" id="tw-f-origin-city" onclick="document.getElementById('f-origin-city').focus()">
                                <input type="text" id="f-origin-city" class="tag-input editorial-input" placeholder="Where did you grow up?" autocomplete="off" style="margin-top:0;">
                            </div>
                            <div class="autocomplete-list" id="autocomplete-f-origin-city"></div>
                        </div>`;
content = content.replace(oldOriginHtml, newOriginHtml);

// 4. btnNext.onclick rewrite (skip conn-X, stop after rec-4)
const oldBtnNextOnclick = /btnNext\.onclick = \(\) => \{[\s\S]*?(?=\};\s*\} else \{)/m;
const newBtnNextOnclick = `btnNext.onclick = () => {
                    if (currentStr === '0') processStep0();
                    else if (currentStr === '4') processStep4();
                    else if (currentStr === '4a') triggerRecommendations(1);
                    else if (currentStr === 'rec-1') {
                        window._nextWizardStep = '5';
                        window._isPartialAdd = true;
                        processStep9();
                    }
                    
                    else if (currentStr === '5') triggerRecommendations(2);
                    else if (currentStr === 'rec-2') {
                        window._nextWizardStep = '6';
                        window._isPartialAdd = true;
                        processStep9();
                    }
                    
                    else if (currentStr === '6') triggerRecommendations(3);
                    else if (currentStr === 'rec-3') {
                        const cityOrigin = getFieldValues('tw-f-origin-city', 'f-origin-city').join(' ').toLowerCase();
                        const cityCurrent = getFieldValues('tw-f-city', 'f-city').join(' ').toLowerCase();
                        const isIsrael = cityOrigin.includes('israel') || cityOrigin.includes('ישראל') || cityCurrent.includes('israel') || cityCurrent.includes('ישראל');
                        window._nextWizardStep = isIsrael ? '7' : '8';
                        window._isPartialAdd = true;
                        processStep9();
                    }
                    
                    else if (currentStr === '7') triggerRecommendations(4);
                    else if (currentStr === 'rec-4') {
                        window._nextWizardStep = null;
                        window._isPartialAdd = false;
                        processStep9();
                    }
                    
                    else if (currentStr === '8') {
                        window._nextWizardStep = null;
                        window._isPartialAdd = false;
                        processStep9();
                    }`;
content = content.replace(oldBtnNextOnclick, newBtnNextOnclick);

// 5. triggerRecommendations logic
const oldTriggerRecs = /function triggerRecommendations\(sessionNum\) \{[\s\S]*?(?=\}\n\n        function buildConnectionsHTML)/m;
const newTriggerRecs = `function triggerRecommendations(sessionNum) {
            let recStep = '';
            if (sessionNum === 1) { recStep = 'rec-1'; }
            else if (sessionNum === 2) { recStep = 'rec-2'; }
            else if (sessionNum === 3) { recStep = 'rec-3'; }
            else if (sessionNum === 4) { recStep = 'rec-4'; }
            
            window._currentConnStep = recStep;
            const hasRecs = generateRecommendations(sessionNum);
            
            if (hasRecs) {
                goToWizardStep(recStep);
            } else {
                if (sessionNum >= 4) {
                    window._isPartialAdd = false;
                    window._nextWizardStep = null;
                } else {
                    if (sessionNum === 1) window._nextWizardStep = '5';
                    else if (sessionNum === 2) window._nextWizardStep = '6';
                    else if (sessionNum === 3) {
                        const cityOrigin = getFieldValues('tw-f-origin-city', 'f-origin-city').join(' ').toLowerCase();
                        const cityCurrent = getFieldValues('tw-f-city', 'f-city').join(' ').toLowerCase();
                        const isIsrael = cityOrigin.includes('israel') || cityOrigin.includes('ישראל') || cityCurrent.includes('israel') || cityCurrent.includes('ישראל');
                        window._nextWizardStep = isIsrael ? '7' : '8';
                    }
                    window._isPartialAdd = true;
                }
                processStep9();
            }
        }`;
content = content.replace(oldTriggerRecs, newTriggerRecs);

// 6. generateRecommendations stepNum filter & ignore current name
const oldGenRecs = /function generateRecommendations\(\) \{[\s\S]*?(?=const p1 = \{)/m;
const newGenRecs = `function generateRecommendations(stepNum) {
            window._addedSomeoneInRecs = false; // reset for this session
            let tags = [];
            
            const addField = (values, prefix) => {
                values.forEach(val => {
                    if (val) tags.push(\`\${prefix}:\${val}\`);
                });
            };
            
            if (stepNum === 1 || !stepNum) {
                addField(getFieldValues('tw-f-city', 'f-city'), 'city');
                addField(getFieldValues('tw-f-origin-city', 'f-origin-city'), 'origincity');
            }
            if (stepNum === 2 || !stepNum) {
                addField(getFieldValues('tw-f-role', 'f-role'), 'role');
            }
            if (stepNum === 3 || !stepNum) {
                if (document.getElementById('f-highschool')) addField([document.getElementById('f-highschool').value], 'highschool');
                if (document.getElementById('f-university')) addField([document.getElementById('f-university').value], 'university');
                if (document.getElementById('f-degree')) addField([document.getElementById('f-degree').value], 'degree');
            }
            if (stepNum === 4 || !stepNum) {
                if (document.getElementById('f-army-role')) addField([document.getElementById('f-army-role').value], 'armyrole');
                if (document.getElementById('f-army-base')) addField([document.getElementById('f-army-base').value], 'armybase');
            }
            
            let calculatedAge = '';
            const byStr = document.getElementById('f-birth-year') ? document.getElementById('f-birth-year').value.trim() : '';
            if (byStr) {
                const byInt = parseInt(byStr);
                if (byInt < 150) {
                    calculatedAge = byStr;
                } else {
                    calculatedAge = (new Date().getFullYear() - byInt).toString();
                }
            }

            `;
content = content.replace(oldGenRecs, newGenRecs);

content = content.replace(
    /const currentName = \(document\.getElementById\('f-name-initial'\) \? document\.getElementById\('f-name-initial'\)\.value : ''\)\.trim\(\)\.toLowerCase\(\);/g,
    `const currentName = (document.getElementById('f-name') ? document.getElementById('f-name').value : '').trim().toLowerCase() || (document.getElementById('f-name-initial') ? document.getElementById('f-name-initial').value : '').trim().toLowerCase();`
);

// 7. Dynamic popup sentences in showNodeInfo
const oldPopupCopy = /let popupCopy = "";[\s\S]*?popupCopy = "You have more connections to discover in the network.";\s*\}/m;
const newPopupCopy = `let popupCopy = "";
                
                if (connectionCount === 0) {
                    popupCopy = "To start, we need more details...";
                } else {
                    popupCopy = "You have more connections to discover in the network.";
                }`;
content = content.replace(oldPopupCopy, newPopupCopy);

fs.writeFileSync(file, content, 'utf8');
