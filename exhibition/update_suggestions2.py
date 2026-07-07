import re
import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert CSS
    css_to_insert = """
            /* --- CIRCLES DESIGN --- */
            .suggested-circle-card {
                position: relative;
                background: #111;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
                padding: 0;
                margin-bottom: 16px;
                display: flex;
                flex-direction: column;
                color: #F5F5F5;
                overflow: hidden;
                animation: fadeInUp 0.3s ease-out;
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
                background: rgba(255, 255, 255, 0.05);
            }
            .circle-title {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 20px;
                font-weight: 500;
                color: #FFF;
                text-wrap: balance;
                margin-bottom: 6px;
                letter-spacing: -0.01em;
            }
            .circle-meta {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 13px;
                color: rgba(255, 255, 255, 0.6);
            }
            .circle-meta span {
                margin: 0 6px;
                opacity: 0.5;
            }
            .circle-toggle {
                font-family: 'Helvetica', Arial, sans-serif;
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                color: rgba(255, 255, 255, 0.8);
                background: rgba(255, 255, 255, 0.1);
                padding: 6px 12px;
                border-radius: 6px;
                transition: 0.2s;
            }
            .circle-header:hover .circle-toggle {
                background: rgba(255, 255, 255, 0.2);
                color: #FFF;
            }
            .circle-content {
                display: none;
                border-top: 1px solid rgba(255,255,255,0.1);
                padding: 20px 30px;
                background: #000;
            }
            .circle-content .suggested-card {
                border: 1px solid rgba(255,255,255,0.1);
                background: #111;
                margin-bottom: 12px;
                box-shadow: none;
                padding: 16px 20px;
                animation: none;
            }
            .circle-content .suggested-card:last-child {
                margin-bottom: 0;
            }
            .circle-content .suggested-name {
                color: #FFF;
            }
            .circle-content .suggested-meta {
                color: rgba(255, 255, 255, 0.6);
            }
            .circle-content .btn-connect-sleek {
                color: #FFF;
                border-color: rgba(255, 255, 255, 0.2);
            }
            .circle-content .btn-connect-sleek:hover {
                background: #FFF !important;
                color: #000 !important;
            }
            .suggested-circle-card .btn-dismiss-rec {
                color: rgba(255, 255, 255, 0.5) !important;
            }
            .suggested-circle-card .btn-dismiss-rec:hover {
                color: #FFF !important;
            }
            body.light-mode .suggested-circle-card {
                filter: invert(1) hue-rotate(180deg) !important;
            }
            
            .suggested-shared-pill {"""

    if "/* --- CIRCLES DESIGN --- */" not in content:
        content = content.replace("            .suggested-shared-pill {", css_to_insert, 1)

    # 2. Update generateRecommendations logic
    start_str = "            scores.sort((a, b) => b.score - a.score);\n            let pendingRecs = scores.map(s => ({person: s.person, shared: s.shared}));"
    end_str = "            // Initially render up to 5 cards\n            for (let i = 0; i < 5; i++) {\n                renderNextCard();\n            }\n            return visibleCount > 0;\n        }"
    
    if start_str not in content or end_str not in content:
        print("Could not find boundaries for JS replacement.")
        sys.exit(1)
        
    start_idx = content.find(start_str)
    end_idx = content.find(end_str) + len(end_str)
    
    new_js = """
            function formatCircleIdentity(conceptStr) {
                let title = conceptStr;
                let subtitle = "Detected from the information you entered";
                
                if (conceptStr.includes(':')) {
                    const parts = conceptStr.split(':');
                    const category = parts[0].toLowerCase().trim();
                    const value = parts.slice(1).join(':').trim();
                    
                    title = value.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                    
                    if (['university', 'degree', 'highschool'].includes(category)) subtitle = "Based on your education";
                    else if (category === 'city' || category === 'origincity') subtitle = "Based on your location";
                    else if (category === 'role') subtitle = "Based on your field";
                    else if (category === 'armyrole', 'armybase'.includes(category)) subtitle = "Based on your military service";
                } else {
                    title = conceptStr.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                    const lower = conceptStr.toLowerCase();
                    if (['design', 'tech', 'law', 'medicine', 'education', 'finance', 'media', 'music', 'sports', 'psychology', 'fashion'].includes(lower)) {
                        subtitle = "Based on your field";
                    }
                }
                
                return { title, subtitle };
            }

            // Group into circles
            const circlesMap = new Map();
            const individuals = [];
            
            scores.forEach(s => {
                s.shared.forEach(concept => {
                    if (!circlesMap.has(concept)) {
                        circlesMap.set(concept, { concept: concept, people: [], score: 0 });
                    }
                    if (!circlesMap.get(concept).people.some(p => p.person.id === s.person.id)) {
                        circlesMap.get(concept).people.push(s);
                        circlesMap.get(concept).score += s.score;
                    }
                });
            });

            const validCircles = [];
            for (const [concept, circle] of circlesMap.entries()) {
                if (circle.people.length >= 2) {
                    circle.people.sort((a, b) => b.score - a.score);
                    validCircles.push(circle);
                }
            }
            validCircles.sort((a, b) => b.score - a.score);

            scores.forEach(s => {
                const belongsToValidCircle = s.shared.some(concept => circlesMap.has(concept) && circlesMap.get(concept).people.length >= 2);
                if (!belongsToValidCircle) {
                    individuals.push({ person: s.person, shared: s.shared, score: s.score });
                }
            });
            individuals.sort((a, b) => b.score - a.score);

            let pendingRecs = [];
            validCircles.forEach(c => pendingRecs.push({ type: 'circle', data: c }));
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
                    
                    const { title, subtitle } = formatCircleIdentity(circle.concept);
                    
                    div.innerHTML = `
                        <button type="button" class="btn-dismiss-rec" title="Dismiss" style="width: 24px; height: 24px; right: 15px; top: 15px; left: auto; padding: 0; margin: 0; min-width: 0; z-index: 10;">✕</button>
                        <div class="circle-header">
                            <div>
                                <div class="circle-title">${title}</div>
                                <div class="circle-meta">${circle.people.length} people <span>•</span> ${subtitle}</div>
                            </div>
                            <div class="circle-toggle">[ VIEW ]</div>
                        </div>
                        <div class="circle-content"></div>
                    `;
                    
                    const header = div.querySelector('.circle-header');
                    const content = div.querySelector('.circle-content');
                    
                    header.addEventListener('click', (e) => {
                        if(e.target.classList.contains('btn-dismiss-rec')) return;
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            div.querySelector('.circle-toggle').innerText = '[ VIEW ]';
                        } else {
                            content.style.display = 'block';
                            div.querySelector('.circle-toggle').innerText = '[ HIDE ]';
                        }
                    });
                    
                    div.querySelector('.btn-dismiss-rec').addEventListener('click', (e) => {
                        e.stopPropagation();
                        window._dismissedRecs = window._dismissedRecs || new Set();
                        circle.people.forEach(p => window._dismissedRecs.add(p.person.name));
                        removeMainCard();
                    });
                    
                    circle.people.forEach(s => {
                        const p = s.person;
                        const pDiv = document.createElement('div');
                        pDiv.className = 'suggested-card';
                        
                        const metaStr = `${p.role || 'Unknown'} <span>•</span> ${p.city || 'Unknown'}`;
                        const metaNoOrphans = metaStr.replace(/ ([^ ]*)$/, '&nbsp;$1');
                        
                        pDiv.innerHTML = `
                            <div class="suggested-card-content">
                                <div class="suggested-name">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                                <div class="suggested-meta">${metaNoOrphans}</div>
                            </div>
                            <div class="suggested-card-action">
                                <button type="button" class="btn-connect-sleek" data-id="${p.id}">[ CONNECT ]</button>
                            </div>
                        `;
                        
                        pDiv.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                            const id = parseInt(e.target.dataset.id);
                            addConnectionEntry(id, 'acquaintance', 3);
                            window._addedSomeoneInRecs = true;
                            pDiv.style.opacity = '0.5';
                            e.target.innerText = '[ ADDED ]';
                            e.target.classList.add('added');
                        });
                        
                        content.appendChild(pDiv);
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
                        <button type="button" class="btn-dismiss-rec" title="Dismiss" style="width: 24px; height: 24px; right: 10px; left: auto; padding: 0; margin: 0; min-width: 0;">✕</button>
                        <div class="suggested-card-content">
                            <div class="suggested-name">${p.name.replace(/ ([^ ]*)$/, '&nbsp;$1')}</div>
                            <div class="suggested-meta">${metaNoOrphans}</div>
                            ${sharedHTML}
                        </div>
                        <div class="suggested-card-action">
                            <button type="button" class="btn-connect-sleek" data-id="${p.id}">[ CONNECT ]</button>
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

            // Initially render up to 5 cards
            for (let i = 0; i < 5; i++) {
                renderNextCard();
            }
            return visibleCount > 0;
        }"""

    content = content[:start_idx] + new_js.strip('\n') + content[end_idx:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated index.html with new styling and titles.")

if __name__ == '__main__':
    main()
