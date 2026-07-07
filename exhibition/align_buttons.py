import sys
import re

def main():
    filepath = '/Users/omerbarak/Documents/פגמר/exhibition/public/index.html'
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the × button styling globally in these templates
    old_x_btn = r"style=\"background:transparent; border:none; color:#000; font-size:24px; cursor:pointer; padding:8px; line-height:0\.8; font-weight:100; opacity:0\.6; outline:none;\""
    new_x_btn = "style=\"background:transparent; border:none; color:#000; font-size:18px; cursor:pointer; padding:4px; line-height:1; font-weight:300; opacity:0.4; outline:none;\""
    
    content = re.sub(old_x_btn, new_x_btn, content)

    # 2. Fix the alignment of the bottom row in the community card
    old_circle_bottom = r"""                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;">
                                <div class="circle-meta" style="font-size: 10px; text-transform: uppercase; letter-spacing: 1\.5px; color: #666; font-weight: 500;">
                                    \$\{circle\.people\.length\} people &middot; Friend &middot; Strength 3
                                </div>
                                <div>
                                    <button type="button" class="circle-toggle info-action-btn" style="margin: 0; font-weight: 300; border: none;">\[ EXPAND \]</button>
                                </div>
                            </div>"""

    new_circle_bottom = """                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                                <div class="circle-meta" style="display: flex; align-items: center; gap: 8px; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500;">
                                    <span>${circle.people.length} people &middot; Friend &middot; Strength 3</span>
                                </div>
                                <div style="display: flex; gap: 10px; align-items: center;">
                                    <button type="button" class="circle-toggle info-action-btn" style="margin: 0; font-weight: 300; border: none;">[ EXPAND ]</button>
                                </div>
                            </div>"""
                            
    content = re.sub(old_circle_bottom, new_circle_bottom, content)

    # 3. Fix the alignment of the bottom row in the individual card
    old_indiv_bottom = r"""                            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 8px;">
                                <div class="circle-meta" style="display: flex; align-items: center; gap: 8px; font-size: 10px; text-transform: uppercase; letter-spacing: 1\.5px; color: #666; font-weight: 500;">
                                    <span>Friend &middot; 3</span>
                                    <button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0\.6; padding: 0;">\[ EDIT \]</button>
                                </div>
                                <div style="display: flex; gap: 10px; align-items: center;">
                                    <button type="button" class="info-action-btn btn-connect-sleek" data-id="\$\{p\.id\}" style="margin: 0; font-weight: 300; border: none;">\[ CONNECT \]</button>
                                </div>
                            </div>"""
                            
    new_indiv_bottom = """                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                                <div class="circle-meta" style="display: flex; align-items: center; gap: 8px; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #666; font-weight: 500;">
                                    <span>Friend &middot; Strength 3</span>
                                    <button type="button" class="btn-customize-person" style="background: transparent; border: none; cursor: pointer; color: #111; font-weight: 500; font-size: 9px; opacity: 0.6; padding: 0;">[ EDIT ]</button>
                                </div>
                                <div style="display: flex; gap: 10px; align-items: center;">
                                    <button type="button" class="info-action-btn btn-connect-sleek" data-id="${p.id}" style="margin: 0; font-weight: 300; border: none;">[ CONNECT ]</button>
                                </div>
                            </div>"""

    content = re.sub(old_indiv_bottom, new_indiv_bottom, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Refined align and dismiss buttons.")

if __name__ == '__main__':
    main()
