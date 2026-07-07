import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix saveEditedPerson to scope querySelector to edit-connections-list and always assign data.connections
old_save_logic = """            // Also collect connections if they were edited
            const connectionDivs = document.querySelectorAll('.connection-entry');
            const connectionsData = Array.from(connectionDivs).map(div => {
                const targetName = div.querySelector('.conn-target').value.trim();
                if (!targetName) return null;
                
                const targetPerson = people.find(p => p.name === targetName);
                if (!targetPerson) return null;
                
                return {
                    id: targetPerson.id,
                    type: div.querySelector('.conn-type').value || 'colleague',
                    strength: parseInt(div.querySelector('.conn-strength').value) || 3
                };
            }).filter(Boolean);
            if (connectionsData.length > 0) {
                data.connections = connectionsData;
            }"""

new_save_logic = """            // Also collect connections if they were edited
            const editConnsList = document.getElementById('edit-connections-list');
            const connectionDivs = editConnsList ? editConnsList.querySelectorAll('.connection-entry') : [];
            const connectionsData = Array.from(connectionDivs).map(div => {
                const targetName = div.querySelector('.conn-target').value.trim();
                if (!targetName) return null;
                
                const targetPerson = people.find(p => p.name === targetName);
                if (!targetPerson) return null;
                
                return {
                    id: targetPerson.id,
                    type: div.querySelector('.conn-type').value || 'colleague',
                    strength: parseInt(div.querySelector('.conn-strength').value) || 3
                };
            }).filter(Boolean);
            
            // Always set data.connections so deletions are saved
            data.connections = connectionsData;"""

if old_save_logic in html:
    html = html.replace(old_save_logic, new_save_logic)
    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed saveEditedPerson logic")
else:
    print("Could not find old save logic to replace")

