import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Step 0 layout
step_0 = """
                <!-- STEP 0 -->
                <div id="wizard-step-0" class="wizard-step active" style="text-align: center; padding-top: 40px;">
                    <h2 class="modal-title">Who are you adding?</h2>
                    <p class="modal-subtitle">Every connection begins with a single thread.</p>
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: #F5F5F5; margin: 0 auto 50px auto; animation: pulse 2s infinite; box-shadow: 0 0 15px rgba(245,245,245,0.5);"></div>
                    <div style="display: flex; gap: 20px; justify-content: center;">
                        <button type="button" class="btn-apple-secondary" onclick="document.getElementById('form-is-myself').value='yes'; window.updateWizardCopy(true); goToWizardStep(1);" style="flex: 1; max-width: 180px;">Myself</button>
                        <button type="button" class="btn-apple-secondary" onclick="document.getElementById('form-is-myself').value='no'; window.updateWizardCopy(false); goToWizardStep(1);" style="flex: 1; max-width: 180px;">Someone Else</button>
                    </div>
                </div>
"""
start_0 = html.find('<!-- STEP 0 -->')
end_0 = html.find('<!-- STEP 1 -->')
if start_0 != -1 and end_0 != -1:
    html = html[:start_0] + step_0 + html[end_0:]


# 2. Add animation style for pulse
if "@keyframes pulse {" not in html:
    pulse_style = """
            @keyframes pulse {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245, 245, 245, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(245, 245, 245, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(245, 245, 245, 0); }
            }
"""
    html = html.replace('</style>', pulse_style + '        </style>')


# 3. Update preview area to SVG
preview_area = """
            <div class="wizard-preview-area" id="wizard-preview-area">
                <svg id="svg-preview" viewBox="-200 -200 400 400">
                    <!-- Base central node -->
                    <circle cx="0" cy="0" r="8" class="organic-node" id="preview-center-node" />
                    <text x="0" y="25" text-anchor="middle" class="organic-label" id="preview-center-label">NEW PATH</text>
                </svg>
            </div>
"""
start_preview = html.find('<div class="wizard-preview-area"')
end_preview = html.find('</div>', html.find('</div>', html.find('</div>', start_preview) + 1) + 1) + 6
# Actually the preview area doesn't have nested divs originally
# Let's find exactly
preview_regex = r'<div class="wizard-preview-area" id="wizard-preview-area">.*?</div>'
html = re.sub(preview_regex, preview_area.strip(), html, flags=re.DOTALL)


# 4. Inject Javascript
js_inject = """
        // UX Functions
        window.updateWizardCopy = function(isMyself) {
            document.getElementById('step-1-title').textContent = isMyself ? "What's your name?" : "What's their name?";
            document.getElementById('f-city').placeholder = isMyself ? "Where do you live?" : "Where do they live?";
            document.getElementById('f-origin-city').placeholder = isMyself ? "Where are you originally from?" : "Where are they originally from?";
            document.getElementById('preview-center-label').textContent = isMyself ? "YOU" : "THEM";
            
            // Clear existing svg nodes
            const svg = document.getElementById('svg-preview');
            const paths = svg.querySelectorAll('path');
            const circles = svg.querySelectorAll('circle:not(#preview-center-node)');
            const texts = svg.querySelectorAll('text:not(#preview-center-label)');
            paths.forEach(p => p.remove());
            circles.forEach(c => c.remove());
            texts.forEach(t => t.remove());
            window.svgNodesCount = 0;
        };

        window.svgNodesCount = 0;
        window.addNodeToOrganicPreview = function(labelStr, valueStr) {
            if(!valueStr) return;
            const svg = document.getElementById('svg-preview');
            window.svgNodesCount++;
            
            const angle = (window.svgNodesCount * 137.5) * (Math.PI / 180); // golden angle
            const radius = 60 + (window.svgNodesCount * 15);
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            
            // Draw path
            const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            path.setAttribute('d', `M 0 0 Q ${x/2} ${y/2 + 20} ${x} ${y}`);
            path.setAttribute('class', 'organic-link');
            
            // Draw circle
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', x);
            circle.setAttribute('cy', y);
            circle.setAttribute('r', '4');
            circle.setAttribute('class', 'organic-node');
            
            // Draw text
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', x);
            text.setAttribute('y', y + 15);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('class', 'organic-label');
            text.textContent = valueStr.substring(0, 15) + (valueStr.length > 15 ? '...' : '');
            
            svg.insertBefore(path, svg.firstChild);
            svg.appendChild(circle);
            svg.appendChild(text);
        };
"""

# Replace old addNodeToPreview
old_addnode = r'function addNodeToPreview\(type, val\) \{.*?\}'
html = re.sub(old_addnode, '', html, flags=re.DOTALL)
html = html.replace('addNodeToPreview(', 'addNodeToOrganicPreview(')

if "window.updateWizardCopy" not in html:
    html = html.replace('window.goToWizardStep = function goToWizardStep(step) {', js_inject + '\n        window.goToWizardStep = function goToWizardStep(step) {')


# 5. Fix HTML Title Classes
html = html.replace('<h2 style="font-weight: 300; margin-bottom: 40px; font-size: 28px;">', '<h2 class="modal-title">')
html = html.replace('<h2 id="step-1-title" style="font-weight: 300; margin-bottom: 40px; font-size: 28px;">', '<h2 id="step-1-title" class="modal-title">')

# Replace inline <p style="..."> with <p class="modal-subtitle">
html = re.sub(r'<p style="color: rgba\(245,245,245,0\.6\); font-size: 14px; margin-bottom: 30px;">', '<p class="modal-subtitle">', html)

# 6. Update generateRecommendations card styling
old_rec_html = """
                const card = document.createElement('div');
                card.style.cssText = "background: rgba(245,245,245,0.05); border: 1px solid rgba(245,245,245,0.1); border-radius: 8px; padding: 15px; margin-bottom: 10px; cursor: pointer; transition: 0.2s;";
"""
new_rec_html = """
                const card = document.createElement('div');
                card.style.cssText = "background: rgba(245,245,245,0.02); border: 1px solid rgba(245,245,245,0.08); border-radius: 12px; padding: 25px; margin-bottom: 15px; cursor: pointer; transition: 0.2s; display: flex; flex-direction: column; gap: 8px;";
"""
html = html.replace(old_rec_html, new_rec_html)

old_card_inner = """
                card.innerHTML = `
                    <div style="font-size: 16px; font-weight: 600;">${p.name}</div>
                    <div style="font-size: 12px; color: rgba(245,245,245,0.7);">${p.role || ''} • ${p.city || ''}</div>
                    <div style="font-size: 12px; color: #a1d1a1; margin-top: 5px;">Shared paths: ${sharedChapters.join(', ')}</div>
                `;
"""
new_card_inner = """
                card.innerHTML = `
                    <div style="font-size: 18px; font-weight: 500; letter-spacing: 0.5px;">${p.name}</div>
                    <div style="font-size: 13px; color: rgba(245,245,245,0.5);">${p.role || ''} • ${p.city || ''}</div>
                    <div style="margin-top: 10px; display: inline-flex; flex-wrap: wrap; gap: 6px;">
                        ${sharedChapters.map(c => `<span style="background: rgba(245,245,245,0.1); padding: 4px 10px; border-radius: 12px; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">${c}</span>`).join('')}
                    </div>
                `;
                card.onmouseover = () => card.style.background = 'rgba(245,245,245,0.05)';
                card.onmouseout = () => card.style.background = 'rgba(245,245,245,0.02)';
"""
html = html.replace(old_card_inner, new_card_inner)


# Write changes
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
