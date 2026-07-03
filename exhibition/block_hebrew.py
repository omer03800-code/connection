import re

def main():
    with open('public/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find a good place to inject the Hebrew blocker.
    # Let's put it near the autocomplete initialization or window load
    target = "document.addEventListener('DOMContentLoaded', () => {"
    replacement = """document.addEventListener('DOMContentLoaded', () => {
            // Block Hebrew characters in all inputs
            document.addEventListener('input', (e) => {
                if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                    if (/[\u0590-\u05FF]/.test(e.target.value)) {
                        e.target.value = e.target.value.replace(/[\u0590-\u05FF]/g, '');
                        // Optional: Show a brief alert or toast
                        // alert('Hebrew is not allowed. Please type in English.');
                    }
                }
            });"""
    content = content.replace(target, replacement)

    with open('public/index.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
