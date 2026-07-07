import sys

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the problematic block:
    old_block = """                    const toggleBtn = div.querySelector('.circle-toggle');
                    
                    const toggleFunc = () => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            headerWrap.style.paddingBottom = '40px';
                            toggleBtn.innerText = '[ EXPAND ]';
                        } else {
                            content.style.display = 'block';
                            headerWrap.style.paddingBottom = '0';
                            toggleBtn.innerText = '[ CLOSE ]';
                        }
                    };
                    
                    toggleBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        toggleFunc();
                    });"""

    new_block = """                    const toggleFunc = () => {
                        if (content.style.display === 'block') {
                            content.style.display = 'none';
                            headerWrap.style.paddingBottom = '48px';
                        } else {
                            content.style.display = 'block';
                            headerWrap.style.paddingBottom = '0';
                        }
                    };"""

    if old_block in content:
        content = content.replace(old_block, new_block)
    else:
        print("Could not find the block to replace")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Fixed toggleBtn bug.")

if __name__ == '__main__':
    main()
