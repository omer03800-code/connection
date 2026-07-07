import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    css_to_insert = """
            /* --- CIRCLES DESIGN V4 --- */
            .suggested-circle-card {
                position: relative;
                background: #FFF;
                border: 1px solid rgba(0,0,0,0.15);
                padding: 0;
                margin-bottom: 24px;
                display: flex;
                flex-direction: column;
                color: #111;
                overflow: hidden;
                animation: fadeInUp 0.4s ease-out;
            }
            .circle-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 24px 30px;
                cursor: pointer;
                transition: background 0.2s;
            }
            .circle-header:hover {
                background: rgba(0, 0, 0, 0.02);
            }
            .circle-title {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 20px;
                font-weight: 400;
                color: #111;
                margin-bottom: 8px;
                letter-spacing: -0.01em;
            }
            .circle-meta {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 13px;
                color: #666;
            }
            .circle-meta span {
                margin: 0 6px;
                opacity: 0.3;
            }
            
            /* Native Button Styles for circles */
            .btn-circle-action {
                background: transparent;
                border: none;
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 11px;
                font-weight: 500;
                letter-spacing: 2px;
                color: #111;
                cursor: pointer;
                padding: 6px 0;
                text-transform: uppercase;
                transition: 0.2s;
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
                border-top: 1px solid rgba(0,0,0,0.06);
                padding: 24px 30px;
                background: #FFF;
            }
            .circle-bulk-actions {
                display: flex;
                gap: 16px;
                margin-bottom: 24px;
            }
            
            /* Mini Individual Card */
            .circle-content .suggested-card {
                border: 1px solid rgba(0,0,0,0.08);
                background: #FFF;
                margin-bottom: 8px;
                padding: 12px 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: none;
                animation: none;
            }
            .circle-content .suggested-card:last-child {
                margin-bottom: 0;
            }
            .circle-content .suggested-card-content {
                display: flex;
                flex-direction: column;
                gap: 2px;
                flex: 1;
            }
            .circle-content .suggested-name {
                font-size: 15px;
                font-weight: 500;
                color: #111;
                margin-bottom: 0;
            }
            .circle-content .suggested-meta {
                font-size: 12px;
                color: #888;
                margin-bottom: 0;
            }
            .circle-content .suggested-reason {
                font-size: 10px;
                color: #888;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 4px;
            }
            .circle-content .suggested-card-action {
                margin-left: 16px;
            }
            
            .suggested-shared-pill {"""

    if "/* --- CIRCLES DESIGN V4 --- */" not in content:
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
                let subtitle = "We found a community from your past";
                
                if (conceptStr.includes(':')) {
                    const parts = conceptStr.split(':');
                    const category = parts[0].toLowerCase().trim();
                    const value = parts.slice(1).join(':').trim();
                    
                    title = value.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                    
                    if (['university', 'degree', 'highschool'].includes(category)) subtitle = "Based on your education";
                    else if (category === 'city' || category === 'origincity') subtitle = "Based on your location";
                    else if (category === 'role') subtitle = "Based on your field";
                    else if (['armyrole', 'armybase'].includes(category)) subtitle = "Based on your military service";
                } else {
                    title = conceptStr.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                    const lower = conceptStr.toLowerCase();
                    if (['design', 'tech', 'law', 'medicine', 'education', 'finance', 'media', 'music', 'sports', 'psychology', 'fashion'].includes(lower)) {
                        subtitle = "Based on your field";
                    }
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
                let intersectionPeople = [...baseCircle.people]; // Start with base people
                
                for (let j = i + 1; j < circlesArray.length; j++) {
                    if (mergedIndices.has(j)) continue;
                    
                    const compareCircle = circlesArray[j];
                    
                    const baseIds = new Set(intersectionPeople.map(p => p.person.id));
                    const compareIds = new Set(compareCircle.people.map(p => p.person.id));
                    
                    const intersection = new Set([...baseIds].filter(x => compareIds.has(x)));
                    const union = new Set([...baseIds, ...compareIds]);
                    
                    const jaccard = intersection.size / union.size;
                    
                    // Only merge if very similar, and strictly keep the INTERSECTION to avoid bringing in strangers
                    if (jaccard >= 0.7 || intersection.size === compareIds.size || intersection.size === baseIds.size) {
                        mergedIndices.add(j);
                        if (!mergedConcepts.includes(compareCircle.concept)) {
                            mergedConcepts.push(compareCircle.concept);
                        }
                        // Restrict circle members to strictly the intersecting people
                        intersectionPeople = intersectionPeople.filter(p => compareIds.has(p.person.id));
                    }
                }
                
                // If intersection wiped everyone out (shouldn't happen with jaccard), fallback to base
                if (intersectionPeople.length < 2) {
                    intersectionPeople = [...baseCircle.people];
                    mergedConcepts = [baseCircle.concept];
                }
                
                const parsedConcepts = mergedConcepts.map(c => parseConcept(c));
                let finalSubtitle = parsedConcepts.find(pc => pc.subtitle !== "We found a community from your past")?.subtitle || "We found a community from your past";
                
                // Filter out generic titles if we have better ones
                const nonGenericTitles = parsedConcepts.map(pc => pc.title).filter(t => !['Student', 'Design', 'Tech'].includes(t));
                let finalTitle = nonGenericTitles.length > 0 ? nonGenericTitles.slice(0, 2).join(' / ') : parsedConcepts[0].title;
                
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
                        <div class="circle-header">
                            <div>
                                <div class="circle-title">${circle.title}</div>
                                <div class="circle-meta">${circle.subtitle}</div>
                            </div>
                            <button type="button" class="btn-circle-action circle-toggle">[ VIEW ]</button>
                        </div>
                        <div class="circle-content">
                            <div class="circle-bulk-actions">
                                <button type="button" class="btn-circle-action btn-bulk-connect">[ CONNECT WITH EVERYONE ]</button>
                                <button type="button" class="btn-circle-action btn-bulk-skip">[ SKIP CIRCLE ]</button>
                            </div>
                            <div class="circle-people-list"></div>
                        </div>
                    `;
                    
                    const header = div.querySelector('.circle-header');
                    const content = div.querySelector('.circle-content');
                    const peopleList = div.querySelector('.circle-people-list');
                    const toggleBtn = div.querySelector('.circle-toggle');
                    
                    header.addEventListener('click', () => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            toggleBtn.innerText = '[ VIEW ]';
                        } else {
                            content.style.display = 'block';
                            toggleBtn.innerText = '[ HIDE ]';
                        }
                    });
                    
                    div.querySelector('.btn-bulk-skip').addEventListener('click', (e) => {
                        e.stopPropagation();
                        window._dismissedRecs = window._dismissedRecs || new Set();
                        circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                        removeMainCard();
                    });

                    div.querySelector('.btn-bulk-connect').addEventListener('click', (e) => {
                        e.stopPropagation();
                        circle.people.forEach(s => {
                            const btn = peopleList.querySelector('[data-id="' + s.person.id + '"]');
                            if (btn && !btn.disabled) {
                                addConnectionEntry(s.person.id, 'acquaintance', 3);
                                btn.innerText = '[ ADDED ]';
                                btn.classList.add('added');
                                btn.disabled = true;
                                btn.closest('.suggested-card').style.opacity = '0.5';
                            }
                        });
                        window._addedSomeoneInRecs = true;
                        e.target.innerText = '[ ADDED ALL ]';
                        e.target.disabled = true;
                    });
                    
                    circle.people.forEach(s => {
                        const p = s.person;
                        const pDiv = document.createElement('div');
                        pDiv.className = 'suggested-card';
                        
                        const metaStr = `${p.role || 'Unknown'} <span>•</span> ${p.city || 'Unknown'}`;
                        const metaNoOrphans = metaStr.replace(/ ([^ ]*)$/, '&nbsp;$1');
                        
                        // Parse connection reasons for this person
                        const personReasons = s.shared.map(c => parseConcept(c).title).join(', ');
                        
                        pDiv.innerHTML = `
                            <div class="suggested-card-content">
                                <div class="suggested-name">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-meta">${metaNoOrphans}</div>
                                <div class="suggested-reason">${personReasons}</div>
                            </div>
                            <div class="suggested-card-action">
                                <button type="button" class="btn-circle-action btn-connect-sleek" data-id="${p.id}">[ CONNECT ]</button>
                            </div>
                        `;
                        
                        pDiv.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                            const id = parseInt(e.target.dataset.id);
                            addConnectionEntry(id, 'acquaintance', 3);
                            window._addedSomeoneInRecs = true;
                            pDiv.style.opacity = '0.5';
                            e.target.innerText = '[ ADDED ]';
                            e.target.classList.add('added');
                            e.target.disabled = true;
                        });
                        
                        peopleList.appendChild(pDiv);
                    });
                    
                    recList.appendChild(div);
                } else {
                    const p = rec.data.person;
                    const sharedConcepts = rec.data.shared || [];
                    div.className = 'suggested-card';
                    div.style.animation = 'fadeInUp 0.3s ease-out';
                    
                    let sharedHTML = '';
                    if (sharedConcepts.length > 0) {
                        const pillsHTML = sharedConcepts.map(c => {
                            const match = c.match(/\\(([^)]+)\\)/);
                            const shortLabel = match ? match[1] : c;
                            return `<span class="suggested-shared-pill">${shortLabel}</span>`;
                        }).join('');
                        sharedHTML = `
                            <div class="suggested-shared-wrap">
                                <span class="suggested-shared-label">SHARED PATHS</span>
                                <div style="display: flex; gap: 8px; flex-wrap: wrap;">${pillsHTML}</div>
                            </div>
                        `;
                    }

                    const metaStr = `${p.role || 'Unknown'} <span>•</span> ${p.city || 'Unknown'}`;
                    const metaNoOrphans = metaStr.replace(/ ([^ ]*)$/, '&nbsp;$1');

                    div.innerHTML = `
                        <button type="button" class="btn-circle-action btn-dismiss-rec" title="Dismiss" style="right: 10px; left: auto; padding: 0; margin: 0;">[ ✕ ]</button>
                        <div class="suggested-card-content">
                            <div class="suggested-name">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                            <div class="suggested-meta">${metaNoOrphans}</div>
                            ${sharedHTML}
                        </div>
                        <div class="suggested-card-action">
                            <button type="button" class="btn-circle-action btn-connect-sleek" data-id="${p.id}">[ CONNECT ]</button>
                        </div>
                    `;
                    recList.appendChild(div);
                    
                    div.querySelector('.btn-dismiss-rec').addEventListener('click', () => {
                        window._dismissedRecs = window._dismissedRecs || new Set();
                        window._dismissedRecs.add(p.name);
                        removeMainCard();
                    });
                    
                    div.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                        const id = parseInt(e.target.dataset.id);
                        addConnectionEntry(id, 'acquaintance', 3);
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
        
    print("Successfully updated index.html with strictly correct grouping and native UX.")

if __name__ == '__main__':
    main()
