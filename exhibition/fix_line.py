with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0.8 });', 'new THREE.MeshBasicMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0.3 });')
html = html.replace('new THREE.CylinderGeometry(0.5, 0.5, dist, 4);', 'new THREE.CylinderGeometry(0.2, 0.2, dist, 4);')

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
