import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the inner block of setupAutocomplete to clean strings
old_code = """
                // Count occurrences from people array
                let counts = {};
                people.forEach(p => {
                    // Check direct fields
                    if (prefix === 'city' && p.city) {
                        const c = p.city.trim();
                        counts[c] = (counts[c] || 0) + 1;
                    } else if (prefix === 'role' && p.role) {
                        const r = p.role.trim();
                        counts[r] = (counts[r] || 0) + 1;
                    }
                    
                    // Check tags
                    if (p.tags) {
                        const tArr = Array.isArray(p.tags) ? p.tags : p.tags.split(',');
                        tArr.forEach(t => {
                            t = t.trim();
                            if (t.toLowerCase().startsWith(prefix + ':')) {
                                const cleanVal = t.substring(prefix.length + 1).trim();
                                counts[cleanVal] = (counts[cleanVal] || 0) + 1;
                            }
                        });
                    }
                });"""

new_code = """
                // Count occurrences from people array
                let counts = {};
                
                const cleanStr = (s) => {
                    if (!s) return "";
                    let cleaned = s.split('—')[0].split('-')[0].split('|')[0].trim();
                    return cleaned;
                };
                
                people.forEach(p => {
                    // Check direct fields
                    if (prefix === 'city' && p.city) {
                        const c = cleanStr(p.city);
                        if(c) counts[c] = (counts[c] || 0) + 1;
                    } else if (prefix === 'role' && p.role) {
                        const r = cleanStr(p.role);
                        if(r) counts[r] = (counts[r] || 0) + 1;
                    }
                    
                    // Check tags
                    if (p.tags) {
                        const tArr = Array.isArray(p.tags) ? p.tags : p.tags.split(',');
                        tArr.forEach(t => {
                            t = t.trim();
                            if (t.toLowerCase().startsWith(prefix + ':')) {
                                const cleanVal = cleanStr(t.substring(prefix.length + 1));
                                if(cleanVal) counts[cleanVal] = (counts[cleanVal] || 0) + 1;
                            }
                        });
                    }
                });"""

html = html.replace(old_code.strip(), new_code.strip())

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
