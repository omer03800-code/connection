import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    css_to_insert = """
            /* --- CIRCLES DESIGN V7 (Reference Image Aesthetic) --- */
            .suggested-circle-card {
                background: #FFF;
                border: 1px solid rgba(0,0,0,0.06);
                border-radius: 8px;
                margin-bottom: 40px;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.02);
                animation: fadeInUp 0.4s ease-out;
            }
            .circle-header-wrap {
                position: relative;
                padding: 40px 40px 0 40px;
            }
            .circle-overline {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 11px;
                color: #666;
                margin-bottom: 12px;
            }
            .circle-title {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 26px;
                font-weight: 400;
                color: #111;
                margin-bottom: 8px;
                letter-spacing: -0.01em;
            }
            .circle-subtitle {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 13px;
                color: #666;
                margin-bottom: 24px;
            }
            .circle-meta {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 12px;
                color: #888;
            }
            .circle-toggle {
                position: absolute;
                top: 40px;
                right: 40px;
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

            .circle-content {
                display: none;
                padding: 0 40px 40px 40px;
                background: #FFF;
            }
            .circle-divider {
                height: 1px;
                background: rgba(0,0,0,0.06);
                margin: 32px 0;
            }
            .circle-bulk-actions {
                display: flex;
                justify-content: center;
                gap: 64px;
                margin-bottom: 32px;
            }
            
            /* Minimal Person Row */
            .circle-content .suggested-card {
                border: 1px solid rgba(0,0,0,0.06);
                background: #FFF;
                border-radius: 6px;
                margin-bottom: 8px;
                padding: 18px 24px;
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
                margin-top: 32px;
            }

            /* Inline Customization Panel (hidden by default, expands on customize) */
            .suggested-card-edit {
                display: none;
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid rgba(0,0,0,0.05);
            }
            .edit-field-group {
                display: flex;
                gap: 32px;
                margin-bottom: 20px;
            }
            .edit-label {
                display: block;
                font-size: 10px;
                text-transform: uppercase;
                color: #888;
                margin-bottom: 8px;
                letter-spacing: 1px;
            }
            .edit-select {
                padding: 10px;
                border: 1px solid #EAEAEA;
                border-radius: 4px;
                background: #FFF;
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 14px;
                color: #111;
                width: 160px;
                outline: none;
            }
            .edit-slider-wrap {
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .edit-slider {
                width: 140px;
                accent-color: #111;
            }
            .edit-slider-val {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 14px;
                color: #111;
                width: 16px;
            }
            
            .suggested-shared-pill {"""

    if "/* --- CIRCLES DESIGN V7" not in content:
        content = content.replace("            .suggested-shared-pill {", css_to_insert, 1)

    start_str = "            scores.sort((a, b) => b.score - a.score);\n            let pendingRecs = scores.map(s => ({person: s.person, shared: s.shared}));"
    end_str = "            // Initially render up to 5 cards\n            for (let i = 0; i < 5; i++) {\n                renderNextCard();\n            }\n            return visibleCount > 0;\n        }"
    
    if start_str not in content or end_str not in content:
        print("Could not find boundaries for JS replacement.")
        sys.exit(1)
        
    start_idx = content.find(start_str)
    end_idx = content.find(end_str) + len(end_str)
    
    new_js = """
            const initialCircles = new Map();
            const individuals = [];
            
            function parseConcept(conceptStr) {
                let title = conceptStr;
                let subtitle = "Community match";
                
                if (conceptStr.includes(':')) {
                    const parts = conceptStr.split(':');
                    const category = parts[0].toLowerCase().trim();
                    const value = parts.slice(1).join(':').trim();
                    title = value.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                } else {
                    title = conceptStr.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                }
                return { title, subtitle };
            }

            scores.forEach(s => {
                s.shared.forEach(concept => {
                    if (!initialCircles.has(concept)) {
                        initialCircles.set(concept, { concept: concept, people: [], score: 0 });
                    }
                    if (!initialCircles.get(concept).people.some(p => p.person.id === s.person.id)) {
                        initialCircles.get(concept).people.push(s);
                        initialCircles.get(concept).score += s.score;
                    }
                });
            });

            const circlesArray = Array.from(initialCircles.values()).filter(c => c.people.length >= 2);
            const mergedCircles = [];
            const mergedIndices = new Set();
            
            for (let i = 0; i < circlesArray.length; i++) {
                if (mergedIndices.has(i)) continue;
                
                let baseCircle = circlesArray[i];
                let mergedConcepts = [baseCircle.concept];
                let intersectionPeople = [...baseCircle.people];
                
                for (let j = i + 1; j < circlesArray.length; j++) {
                    if (mergedIndices.has(j)) continue;
                    
                    const compareCircle = circlesArray[j];
                    const baseIds = new Set(intersectionPeople.map(p => p.person.id));
                    const compareIds = new Set(compareCircle.people.map(p => p.person.id));
                    const intersection = new Set([...baseIds].filter(x => compareIds.has(x)));
                    const union = new Set([...baseIds, ...compareIds]);
                    const jaccard = intersection.size / union.size;
                    
                    if (jaccard >= 0.7 || intersection.size === compareIds.size || intersection.size === baseIds.size) {
                        mergedIndices.add(j);
                        if (!mergedConcepts.includes(compareCircle.concept)) {
                            mergedConcepts.push(compareCircle.concept);
                        }
                        intersectionPeople = intersectionPeople.filter(p => compareIds.has(p.person.id));
                    }
                }
                
                if (intersectionPeople.length < 2) {
                    intersectionPeople = [...baseCircle.people];
                    mergedConcepts = [baseCircle.concept];
                }
                
                const parsedConcepts = mergedConcepts.map(c => parseConcept(c));
                const nonGenericTitles = parsedConcepts.map(pc => pc.title).filter(t => !['Student', 'Design', 'Tech'].includes(t));
                let finalTitle = nonGenericTitles.length > 0 ? nonGenericTitles.slice(0, 2).join(' / ') : parsedConcepts[0].title;
                
                let finalSubtitle = parsedConcepts.map(pc => pc.title).join(' · ');
                if (finalSubtitle === finalTitle) finalSubtitle = "Discovered connections";
                
                mergedCircles.push({
                    title: finalTitle,
                    subtitle: finalSubtitle,
                    people: intersectionPeople.sort((a, b) => b.score - a.score),
                    score: intersectionPeople.reduce((sum, p) => sum + p.score, 0)
                });
            }
            
            mergedCircles.sort((a, b) => b.score - a.score);

            scores.forEach(s => {
                let belongsToValidCircle = false;
                for (const mc of mergedCircles) {
                    if (mc.people.some(p => p.person.id === s.person.id)) {
                        belongsToValidCircle = true;
                        break;
                    }
                }
                if (!belongsToValidCircle) {
                    individuals.push({ person: s.person, shared: s.shared, score: s.score });
                }
            });
            individuals.sort((a, b) => b.score - a.score);

            let pendingRecs = [];
            mergedCircles.forEach(c => pendingRecs.push({ type: 'circle', data: c }));
            individuals.forEach(ind => pendingRecs.push({ type: 'individual', data: ind }));
            
            const recList = document.getElementById('recommendation-list');
            recList.innerHTML = '';
            
            if (pendingRecs.length === 0) {
                return false;
            }
            
            let visibleCount = 0;
            let currentRecIndex = 0;

            const renderNextCard = () => {
                if (currentRecIndex >= pendingRecs.length) return;
                if (visibleCount >= 5) return;

                const rec = pendingRecs[currentRecIndex];
                currentRecIndex++;
                visibleCount++;

                const div = document.createElement('div');
                
                const handleNextLogic = () => {
                    if (currentRecIndex >= pendingRecs.length && visibleCount === 0) {
                        if (window._addedSomeoneInRecs) {
                            goToWizardStep(window._currentConnStep || 'conn-1');
                        } else {
                            const currentConn = window._currentConnStep || 'conn-1';
                            document.querySelectorAll('.wizard-step.active').forEach(el => el.classList.remove('active'));
                            const nextStepEl = document.getElementById('wizard-step-' + currentConn);
                            if (nextStepEl) nextStepEl.classList.add('active');
                            document.getElementById('btn-wizard-global-next').click();
                        }
                    } else {
                        renderNextCard();
                    }
                };
                
                const removeMainCard = () => {
                    div.style.transition = 'all 0.3s ease';
                    div.style.opacity = '0';
                    div.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        div.remove();
                        visibleCount--;
                        handleNextLogic();
                    }, 300);
                };

                if (rec.type === 'circle') {
                    const circle = rec.data;
                    div.className = 'suggested-circle-card';
                    
                    div.innerHTML = `
                        <div class="circle-header-wrap">
                            <div class="circle-overline">We found a community you may already belong to.</div>
                            <div class="circle-title">${circle.title}</div>
                            <div class="circle-subtitle">${circle.subtitle}</div>
                            <div class="circle-meta">${circle.people.length} suggested connections &middot; Friends, 3</div>
                            <button type="button" class="btn-circle-action circle-toggle">[ CLOSE ] ^</button>
                        </div>
                        <div class="circle-content" style="display: block;">
                            <div class="circle-divider"></div>
                            <div class="circle-bulk-actions">
                                <button type="button" class="btn-circle-action btn-bulk-partial">[ I KNOW SOME ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-connect">[ CONNECT WITH EVERYONE ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">[ SKIP CIRCLE ]</button>
                            </div>
                            <div class="circle-people-list"></div>
                            <div class="circle-footer">
                                <button type="button" class="btn-circle-action btn-bulk-customize">[ CUSTOMIZE CONNECTIONS ]</button>
                            </div>
                        </div>
                    `;
                    
                    const headerWrap = div.querySelector('.circle-header-wrap');
                    const content = div.querySelector('.circle-content');
                    const peopleList = div.querySelector('.circle-people-list');
                    const toggleBtn = div.querySelector('.circle-toggle');
                    
                    const toggleFunc = () => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            headerWrap.style.paddingBottom = '40px';
                            toggleBtn.innerText = '[ OPEN ] v';
                        } else {
                            content.style.display = 'block';
                            headerWrap.style.paddingBottom = '0';
                            toggleBtn.innerText = '[ CLOSE ] ^';
                        }
                    };
                    
                    toggleBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleFunc();
                    });
                    
                    div.querySelector('.btn-bulk-skip').addEventListener('click', (e) => {
                        e.stopPropagation();
                        window._dismissedRecs = window._dismissedRecs || new Set();
                        circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                        removeMainCard();
                    });
                    
                    div.querySelector('.btn-bulk-partial').addEventListener('click', (e) => {
                        e.stopPropagation();
                        // Allows manual individual selection if needed via customize
                        div.querySelector('.btn-bulk-customize').click();
                    });

                    div.querySelector('.btn-bulk-connect').addEventListener('click', (e) => {
                        e.stopPropagation();
                        circle.people.forEach(s => {
                            const pCard = peopleList.querySelector('[data-person-id="' + s.person.id + '"]');
                            if (pCard && !pCard.classList.contains('is-added')) {
                                addConnectionEntry(s.person.id, 'friend', 3);
                                pCard.classList.add('is-added');
                                pCard.style.opacity = '0.5';
                                const editPanel = pCard.querySelector('.suggested-card-edit');
                                if (editPanel) editPanel.style.display = 'none';
                            }
                        });
                        window._addedSomeoneInRecs = true;
                        e.target.innerText = '[ ADDED ALL ]';
                        e.target.disabled = true;
                    });
                    
                    div.querySelector('.btn-bulk-customize').addEventListener('click', (e) => {
                        e.stopPropagation();
                        // Open all inline editors inside this circle
                        const editors = peopleList.querySelectorAll('.suggested-card-edit');
                        editors.forEach(ed => ed.style.display = 'block');
                        e.target.style.display = 'none'; // hide the customize button once open
                    });
                    
                    circle.people.forEach(s => {
                        const p = s.person;
                        const pDiv = document.createElement('div');
                        pDiv.className = 'suggested-card';
                        pDiv.setAttribute('data-person-id', p.id);
                        
                        pDiv.innerHTML = `
                            <div class="suggested-card-main">
                                <div class="suggested-name">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-status" style="font-size:11px; color:#888;"></div>
                            </div>
                            <div class="suggested-card-edit">
                                <div class="edit-field-group">
                                    <div>
                                        <label class="edit-label">Connection Type</label>
                                        <select class="edit-select type-input">
                                            <option value="close_family">Close Family</option>
                                            <option value="family">Family</option>
                                            <option value="friend" selected>Friend</option>
                                            <option value="acquaintance">Acquaintance</option>
                                            <option value="professional">Professional</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="edit-label">Strength (1-5)</label>
                                        <div class="edit-slider-wrap">
                                            <input type="range" class="edit-slider strength-input" min="1" max="5" value="3">
                                            <span class="edit-slider-val strength-display">3</span>
                                        </div>
                                    </div>
                                </div>
                                <div style="display:flex; justify-content: flex-end; gap: 16px;">
                                    <button type="button" class="btn-circle-action btn-remove-custom">[ CANCEL ]</button>
                                    <button type="button" class="btn-circle-action btn-save-custom">[ SAVE CONNECTION ]</button>
                                </div>
                            </div>
                        `;
                        
                        const editPanel = pDiv.querySelector('.suggested-card-edit');
                        const statusDisplay = pDiv.querySelector('.suggested-status');
                        const strengthSlider = pDiv.querySelector('.strength-input');
                        const strengthDisplay = pDiv.querySelector('.strength-display');
                        const typeInput = pDiv.querySelector('.type-input');
                        
                        strengthSlider.addEventListener('input', (e) => {
                            strengthDisplay.innerText = e.target.value;
                        });
                        
                        pDiv.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                            editPanel.style.display = 'none';
                        });
                        
                        pDiv.querySelector('.btn-save-custom').addEventListener('click', (e) => {
                            const selType = typeInput.value;
                            const selStrength = parseInt(strengthSlider.value);
                            
                            addConnectionEntry(p.id, selType, selStrength);
                            window._addedSomeoneInRecs = true;
                            
                            statusDisplay.innerText = `[ ADDED ]`;
                            pDiv.classList.add('is-added');
                            pDiv.style.opacity = '0.5';
                            pDiv.style.borderColor = 'transparent';
                            editPanel.style.display = 'none';
                        });
                        
                        peopleList.appendChild(pDiv);
                    });
                    
                    recList.appendChild(div);
                } else {
                    const p = rec.data.person;
                    div.className = 'suggested-circle-card';
                    
                    div.innerHTML = `
                        <div class="circle-header-wrap" style="padding-bottom:40px;">
                            <div class="circle-overline">We found a connection you may know.</div>
                            <div class="circle-title" style="margin-bottom:0;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                        </div>
                        <div class="circle-content" style="display:block; border-top: none;">
                            <div class="circle-divider" style="margin-top:0;"></div>
                            <div class="circle-bulk-actions">
                                <button type="button" class="btn-circle-action btn-connect-sleek" data-id="${p.id}">[ CONNECT ]</button>
                                <button type="button" class="btn-circle-action btn-customize">[ CUSTOMIZE ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">[ DISMISS ]</button>
                            </div>
                            <div class="suggested-card-edit">
                                <div class="edit-field-group">
                                    <div>
                                        <label class="edit-label">Connection Type</label>
                                        <select class="edit-select type-input">
                                            <option value="close_family">Close Family</option>
                                            <option value="family">Family</option>
                                            <option value="friend" selected>Friend</option>
                                            <option value="acquaintance">Acquaintance</option>
                                            <option value="professional">Professional</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label class="edit-label">Strength (1-5)</label>
                                        <div class="edit-slider-wrap">
                                            <input type="range" class="edit-slider strength-input" min="1" max="5" value="3">
                                            <span class="edit-slider-val strength-display">3</span>
                                        </div>
                                    </div>
                                </div>
                                <div style="display:flex; justify-content: flex-end; gap: 16px;">
                                    <button type="button" class="btn-circle-action btn-remove-custom">[ CANCEL ]</button>
                                    <button type="button" class="btn-circle-action btn-save-custom">[ SAVE CONNECTION ]</button>
                                </div>
                            </div>
                        </div>
                    `;
                    recList.appendChild(div);
                    
                    const editPanel = div.querySelector('.suggested-card-edit');
                    const strengthSlider = div.querySelector('.strength-input');
                    const strengthDisplay = div.querySelector('.strength-display');
                    const typeInput = div.querySelector('.type-input');
                    
                    strengthSlider.addEventListener('input', (e) => {
                        strengthDisplay.innerText = e.target.value;
                    });
                    
                    div.querySelector('.btn-bulk-skip').addEventListener('click', () => {
                        window._dismissedRecs = window._dismissedRecs || new Set();
                        window._dismissedRecs.add(p.name);
                        removeMainCard();
                    });
                    
                    div.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                        addConnectionEntry(p.id, 'friend', 3);
                        window._addedSomeoneInRecs = true;
                        removeMainCard();
                    });
                    
                    div.querySelector('.btn-customize').addEventListener('click', (e) => {
                        editPanel.style.display = 'block';
                    });
                    
                    div.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                        editPanel.style.display = 'none';
                    });
                    
                    div.querySelector('.btn-save-custom').addEventListener('click', (e) => {
                        const selType = typeInput.value;
                        const selStrength = parseInt(strengthSlider.value);
                        addConnectionEntry(p.id, selType, selStrength);
                        window._addedSomeoneInRecs = true;
                        removeMainCard();
                    });
                }
            };

            for (let i = 0; i < 5; i++) {
                renderNextCard();
            }
            return visibleCount > 0;
        }"""

    content = content[:start_idx] + new_js.strip('\n') + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated index.html with reference image aesthetics.")

if __name__ == '__main__':
    main()
