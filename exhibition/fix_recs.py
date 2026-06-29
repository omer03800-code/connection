import re

with open('public/index.html', 'r') as f:
    content = f.read()

# 1. Fix Step 8 Continue logic
old_step_8 = """                    else if (step === 8) {
                        if (window._isPartialAdd) {
                            const addForm = document.getElementById('add-form');
                            if (addForm) addForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
                        } else {
                            goToWizardStep(9);
                        }
                    }"""
new_step_8 = """                    else if (step === 8) {
                        goToWizardStep(9);
                    }"""
if old_step_8 in content:
    content = content.replace(old_step_8, new_step_8)

# 2. Fix generateRecommendations rendering
old_recs_render = """            const recsToRender = pendingRecs.slice(0, 5);
            recsToRender.forEach(rec => {
                const p = rec.person;
                const sharedConcepts = rec.shared || [];
                const div = document.createElement('div');
                div.className = 'suggested-card';
                
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
                // Bulletproof anti-orphan: replace the last space with a non-breaking space
                const metaNoOrphans = metaStr.replace(/ ([^ ]*)$/, '&nbsp;$1');

                div.innerHTML = `
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
                
                div.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                    const id = parseInt(e.target.dataset.id);
                    addConnectionEntry(id, 'acquaintance', 3);
                    e.target.textContent = '[ ADDED ]';
                    e.target.classList.add('added');
                    e.target.disabled = true;
                });
            });"""

new_recs_render = """            let visibleCount = 0;
            let currentRecIndex = 0;

            const renderNextCard = () => {
                if (currentRecIndex >= pendingRecs.length) return;
                if (visibleCount >= 5) return;

                const rec = pendingRecs[currentRecIndex];
                currentRecIndex++;
                visibleCount++;

                const p = rec.person;
                const sharedConcepts = rec.shared || [];
                const div = document.createElement('div');
                div.className = 'suggested-card';
                // Add an entrance animation class if you like
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
                
                div.querySelector('.btn-connect-sleek').addEventListener('click', (e) => {
                    const id = parseInt(e.target.dataset.id);
                    addConnectionEntry(id, 'acquaintance', 3);
                    
                    // Remove this card with a fade out
                    div.style.transition = 'all 0.3s ease';
                    div.style.opacity = '0';
                    div.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        div.remove();
                        visibleCount--;
                        renderNextCard(); // Pop up the next one!
                    }, 300);
                });
            };

            // Initially render up to 5 cards
            for (let i = 0; i < 5; i++) {
                renderNextCard();
            }"""

if old_recs_render in content:
    content = content.replace(old_recs_render, new_recs_render)

with open('public/index.html', 'w') as f:
    f.write(content)

