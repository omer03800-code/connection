import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_func = """        function generateRecommendations() {
            let tags = document.getElementById('f-tags').value.split(',').map(t => t.trim()).filter(Boolean);
            const desc = document.getElementById('f-desc').value.trim();
            if (tags.length === 0 && desc) {
                const words = desc.split(/[\s,.-]+/);
                const ignoreWords = ['this','that','with','from','they','the','and','for','was','not','are','but','you','all','any','can','her','him','out'];
                const keywords = words.filter(w => w.length > 3 && !ignoreWords.includes(w.toLowerCase())).slice(0, 4);
                tags = keywords.map(w => '#' + w.replace(/[^a-zA-Zא-ת]/g, ''));
            }

            const p1 = {
                age: document.getElementById('f-age') ? document.getElementById('f-age').value.trim() : '',
                city: document.getElementById('f-city') ? document.getElementById('f-city').value.trim() : '',
                role: document.getElementById('f-role') ? document.getElementById('f-role').value.trim() : '',
                description: desc,
                tags: tags
            };
            
            let scores = [];
            people.forEach(p => {
                const result = calculateMatchScore(p1, p);
                if (result.score >= 15) {
                    scores.push({ person: p, score: result.score, shared: result.sharedConcepts });
                }
            });
            
            scores.sort((a, b) => b.score - a.score);
            let pendingRecs = scores.map(s => ({person: s.person, shared: s.shared}));
            
            const recList = document.getElementById('recommendation-list');
            recList.innerHTML = '';
            
            if (pendingRecs.length === 0) {
                document.getElementById('wizard-step-8').style.display = 'none'; // skip
                goToWizardStep(9);
                return;
            }
            
            const recsToRender = pendingRecs.slice(0, 5);
            recsToRender.forEach(rec => {
                const p = rec.person;
                const sharedConcepts = rec.shared || [];
                const div = document.createElement('div');
                div.style.cssText = 'background: rgba(245,245,245,0.05); border: 1px solid rgba(245,245,245,0.2); border-radius: 10px; padding: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; transition: 0.3s; flex-direction: column; gap: 10px; align-items: stretch;';
                
                let sharedHTML = '';
                if (sharedConcepts.length > 0) {
                    sharedHTML = `<div style="font-size: 11px; color: #4CAF50; background: rgba(76, 175, 80, 0.1); padding: 4px 8px; border-radius: 4px; display: inline-block;">Shared: ${sharedConcepts.join(', ')}</div>`;
                }

                div.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 16px; font-weight: bold; color: #F5F5F5;">${p.name}</div>
                            <div style="font-size: 12px; color: rgba(245,245,245,0.6);">${p.role || ''} • ${p.city || ''}</div>
                        </div>
                        <button type="button" class="btn-add-rec" data-id="${p.id}" style="background: white; color: black; border: none; padding: 8px 16px; border-radius: 10px; font-weight: bold; font-size: 12px; cursor: pointer;">Connect</button>
                    </div>
                    ${sharedHTML}
                `;
                recList.appendChild(div);
                
                div.querySelector('.btn-add-rec').addEventListener('click', (e) => {
                    const id = parseInt(e.target.dataset.id);
                    addConnectionEntry(id, 'acquaintance', 3);
                    e.target.textContent = 'Added';
                    e.target.style.background = '#333';
                    e.target.style.color = '#fff';
                    e.target.disabled = true;
                });
            });
        }"""

start_idx = html.find('        function generateRecommendations() {')
end_idx = html.find('        function openModal(mode, personData = null, defaultConnectionNodeId = null) {')

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + new_func + '\n\n' + html[end_idx:]
    
    # Also fix the wizard-step-6-original-parent -> 9
    new_html = new_html.replace('document.getElementById(\'wizard-step-6-original-parent\').appendChild(document.getElementById(\'connections-section\'));', 'document.getElementById(\'wizard-step-9-original-parent\').appendChild(document.getElementById(\'connections-section\'));')
    new_html = new_html.replace('goToWizardStep(1);', 'goToWizardStep(0);')
    
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Success")
else:
    print("Could not find boundaries")
