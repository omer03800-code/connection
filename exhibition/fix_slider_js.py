import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_sig = "// Strength slider label update"
end_sig = "div.querySelector('.btn-remove-conn').addEventListener('click', () => {"

start_idx = html.find(start_sig)
end_idx = html.find(end_sig, start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find bounds")
    exit(1)

clean_code = """// Strength slider label update
            const strSlider = div.querySelector('.strength-slider') || div.querySelector('.light-slider');
            const strLabel = div.querySelector('.conn-strength-label') || div.querySelector('.light-slider-val');
            if (strSlider && strLabel) {
                const updateSliderLabel = () => {
                    const val = strSlider.value;
                    strLabel.textContent = val;
                    if (strLabel.classList.contains('conn-strength-label')) {
                        const percent = (val - 1) / 4 * 100;
                        strLabel.style.left = `calc(${percent}% + (${10 - percent * 0.2}px))`;
                    }
                };
                strSlider.addEventListener('input', updateSliderLabel);
                updateSliderLabel(); // initial position
            }
            
            """

new_html = html[:start_idx] + clean_code + html[end_idx:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Fixed slider JS successfully")
