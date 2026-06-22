import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_logic = """
            // Conditional Israel logic
            if (country === 'israel' || country === 'il' || country === 'ישראל') {
                document.getElementById('israel-military-section').style.display = 'block';
                document.getElementById('israel-extra-section').style.display = 'block';
            } else {
                document.getElementById('israel-military-section').style.display = 'none';
                document.getElementById('israel-extra-section').style.display = 'none';
            }"""

new_logic = """
            // Conditional Israel logic
            const isIsrael = (country === 'israel' || country === 'il' || country === 'ישראל');
            document.querySelectorAll('.israel-only').forEach(opt => {
                // If it's already selected and removed from the dropdown, don't show it again.
                // But wait, they are just options in the select. We can simply hide/show them.
                if (isIsrael) {
                    opt.style.display = 'block';
                } else {
                    opt.style.display = 'none';
                    // also hide the block if it was somehow added
                    const id = opt.value;
                    const block = document.getElementById('block-' + id);
                    if (block && block.parentElement.id !== 'hidden-chapters') {
                        document.getElementById('hidden-chapters').appendChild(block);
                        document.getElementById('f-' + id).value = '';
                    }
                }
            });"""

html = html.replace(old_code.strip(), new_code.strip()) # wait, old_code is not defined here.
