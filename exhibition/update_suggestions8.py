import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Replace Wizard HTML headers
    old_wizard_html = """<div id="wizard-step-rec" class="wizard-step">
                    <h2>Let's start building your network</h2>
                    <p class="step-explanation">We found a few people who may already be part of it.</p>"""
                    
    new_wizard_html = """<div id="wizard-step-rec" class="wizard-step">
                    <h2 style="font-size: 32px; font-weight: 500; letter-spacing: -0.5px; margin-bottom: 8px;">Let's find your people.</h2>
                    <p class="step-explanation" style="font-size: 15px; margin-bottom: 32px;">We found a few groups you might already have in common with people.</p>"""
                    
    if old_wizard_html in content:
        content = content.replace(old_wizard_html, new_wizard_html)

    # Step 2: Replace CSS
    css_start = "/* --- CIRCLES DESIGN V7 (Reference Image Aesthetic) --- */"
    css_end = ".suggested-shared-pill {"
    
    if css_start in content and css_end in content:
        start_idx = content.find(css_start)
        end_idx = content.find(css_end)
        
        new_css = """/* --- CIRCLES DESIGN V8 (Expandable List) --- */
            #recommendation-list {
                display: flex;
                flex-direction: column;
                gap: 12px;
                padding-right: 180px;
                overflow-y: auto;
                max-height: 70vh;
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
                padding: 24px;
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
                pointer-events: none; /* Let parent row handle clicks if needed, or button */
            }
            .circle-content {
                display: none;
                padding: 0 24px 24px 24px;
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

            /* Inline Customization Panel */
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
            
            """
        content = content[:start_idx] + new_css + content[end_idx:]

    # Step 3: Replace JS logic for evaluateRecommendations
    js_start = "            const initialCircles = new Map();"
    js_end = "            // Initially render up to 5 cards\n            for (let i = 0; i < 5; i++) {\n                renderNextCard();\n            }\n            return visibleCount > 0;\n        }"
    
    if js_start in content and js_end in content:
        start_idx = content.find(js_start)
        end_idx = content.find(js_end) + len(js_end)
        
        new_js = """
            const initialCircles = new Map();
            const individuals = [];
            
            const categoryWeight = {
                'university': 5,
                'highschool': 4,
                'city': 3,
                'origincity': 3,
                'workplace': 2,
                'role': 1,
                'armybase': 2,
                'armyrole': 1
            };
            
            function parseConcept(conceptStr) {
                let title = conceptStr;
                let subtitle = "Looks like you might share this community.";
                let category = "general";
                
                if (conceptStr.includes(':')) {
                    const parts = conceptStr.split(':');
                    category = parts[0].toLowerCase().trim();
                    const value = parts.slice(1).join(':').trim();
                    title = value.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                    
                    if (category === 'university') subtitle = `Looks like you studied together.`;
                    else if (category === 'highschool') subtitle = `Here are a few more people who studied at ${title} around your age.`;
                    else if (category === 'origincity' || category === 'city') subtitle = `You both grew up in ${title}. Know each other?`;
                    else if (category === 'workplace') subtitle = `Looks like you worked together at ${title}.`;
                } else {
                    title = conceptStr.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                }
                return { title, subtitle, category };
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
                
                // Prioritize best concept title based on category weights
                const parsedConcepts = mergedConcepts.map(c => parseConcept(c));
                parsedConcepts.sort((a, b) => (categoryWeight[b.category] || 0) - (categoryWeight[a.category] || 0));
                
                const bestConcept = parsedConcepts[0];
                let finalTitle = bestConcept.title;
                let finalSubtitle = bestConcept.subtitle;
                let weight = categoryWeight[bestConcept.category] || 0;
                
                mergedCircles.push({
                    title: finalTitle,
                    subtitle: finalSubtitle,
                    weight: weight,
                    people: intersectionPeople.sort((a, b) => b.score - a.score),
                    score: intersectionPeople.reduce((sum, p) => sum + p.score, 0)
                });
            }
            
            // Order by confidence: weight first, then score
            mergedCircles.sort((a, b) => {
                if (b.weight !== a.weight) return b.weight - a.weight;
                return b.score - a.score;
            });

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

            pendingRecs.forEach(rec => {
                const div = document.createElement('div');
                div.className = 'suggested-circle-card';
                
                if (rec.type === 'circle') {
                    const circle = rec.data;
                    div.innerHTML = `
                        <div class="circle-header-wrap">
                            <div class="circle-title">${circle.title}</div>
                            <div class="circle-context-row">
                                <div class="circle-subtitle">${circle.subtitle}</div>
                                <button type="button" class="circle-toggle">EXPAND</button>
                            </div>
                            <div class="circle-meta">${circle.people.length} people &middot; Friends</div>
                        </div>
                        <div class="circle-content">
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
                    
                    headerWrap.addEventListener('click', (e) => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            toggleBtn.innerText = 'EXPAND';
                        } else {
                            content.style.display = 'block';
                            toggleBtn.innerText = 'COLLAPSE';
                        }
                    });
                    
                    div.querySelector('.btn-bulk-skip').addEventListener('click', (e) => {
                        e.stopPropagation();
                        window._dismissedRecs = window._dismissedRecs || new Set();
                        circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                        div.style.opacity = '0.5';
                        content.style.display = 'none';
                        toggleBtn.innerText = 'SKIPPED';
                    });
                    
                    div.querySelector('.btn-bulk-partial').addEventListener('click', (e) => {
                        e.stopPropagation();
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
                        const editors = peopleList.querySelectorAll('.suggested-card-edit');
                        editors.forEach(ed => ed.style.display = 'block');
                        e.target.style.display = 'none'; 
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
                                    <button type="button" class="btn-circle-action btn-remove-custom">[ REMOVE ]</button>
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
                            pDiv.style.display = 'none'; // Essentially removing from circle visually
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
                    div.innerHTML = `
                        <div class="circle-header-wrap" style="padding-bottom:24px;">
                            <div class="circle-title" style="margin-bottom:0;">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                            <div class="circle-context-row" style="margin-top:12px; margin-bottom:0;">
                                <div class="circle-subtitle">We found a connection you may know.</div>
                                <button type="button" class="circle-toggle">EXPAND</button>
                            </div>
                        </div>
                        <div class="circle-content">
                            <div class="circle-bulk-actions">
                                <button type="button" class="btn-circle-action btn-connect-sleek" data-id="${p.id}">[ CONNECT ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">[ DISMISS ]</button>
                            </div>
                            <div class="suggested-card-edit" style="display:block; border-top:none; margin-top:0;">
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
                    
                    const headerWrap = div.querySelector('.circle-header-wrap');
                    const content = div.querySelector('.circle-content');
                    const toggleBtn = div.querySelector('.circle-toggle');
                    
                    headerWrap.addEventListener('click', (e) => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            toggleBtn.innerText = 'EXPAND';
                        } else {
                            content.style.display = 'block';
                            toggleBtn.innerText = 'COLLAPSE';
                        }
                    });

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
                        div.style.opacity = '0.5';
                        content.style.display = 'none';
                        toggleBtn.innerText = 'DISMISSED';
                    });
                    
                    div.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                        addConnectionEntry(p.id, 'friend', 3);
                        window._addedSomeoneInRecs = true;
                        div.style.opacity = '0.5';
                        content.style.display = 'none';
                        toggleBtn.innerText = 'ADDED';
                    });
                    
                    div.querySelector('.btn-remove-custom').addEventListener('click', (e) => {
                        content.style.display = 'none';
                        toggleBtn.innerText = 'EXPAND';
                    });
                    
                    div.querySelector('.btn-save-custom').addEventListener('click', (e) => {
                        const selType = typeInput.value;
                        const selStrength = parseInt(strengthSlider.value);
                        addConnectionEntry(p.id, selType, selStrength);
                        window._addedSomeoneInRecs = true;
                        div.style.opacity = '0.5';
                        content.style.display = 'none';
                        toggleBtn.innerText = 'ADDED';
                    });
                }
            });

            return true;
        }"""
        
        content = content[:start_idx] + new_js.strip('\n') + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated index.html with new list layout logic.")

if __name__ == '__main__':
    main()
