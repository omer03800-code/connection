import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_func = """        window.svgNodesCount = 0;
        window.addNodeToOrganicPreview = function(labelStr, valueStr) {
            if(!valueStr) return;
            const svg = document.getElementById('svg-preview');
            if(!svg) return;
            
            if (labelStr === 'Name') {
                const centerLabel = document.getElementById('preview-center-label');
                if (centerLabel) {
                    centerLabel.textContent = valueStr.substring(0, 15) + (valueStr.length > 15 ? '...' : '');
                }
                return;
            }
            
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
        };"""

pattern = r'window\.svgNodesCount = 0;\s*window\.addNodeToOrganicPreview = function\(labelStr, valueStr\) \{.*?svg\.appendChild\(text\);\s*\};'
html = re.sub(pattern, new_func, html, flags=re.DOTALL)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
