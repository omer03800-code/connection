import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_sig = "if (isCompact) {"
end_sig = "// Name Autocomplete"

start_idx = html.find(start_sig)
end_idx = html.find(end_sig, start_idx)

if start_idx == -1 or end_idx == -1:
    print("Could not find bounds")
    exit(1)

clean_code = """if (isCompact) {
                div.style.background = '#fdfdfd';
                div.style.border = '1px solid rgba(0,0,0,0.06)';
                div.style.borderRadius = '8px';
                div.style.padding = '8px 12px';
                div.style.marginBottom = '8px';
                div.style.position = 'relative';
                
                div.innerHTML = `
                    <style>
                    .light-slider { -webkit-appearance: none; width: 100%; height: 4px; border-radius: 2px; background: rgba(0,0,0,0.1); outline: none; }
                    .light-slider::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 12px; height: 12px; border-radius: 50%; background: #111; cursor: pointer; }
                    </style>
                    <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
                        <!-- Left side: Name input & Autocomplete -->
                        <div style="flex: 1; min-width: 60px; display: flex; flex-direction: column; position: relative;">
                            <input type="text" class="conn-target" placeholder="Search Name..." value="${defaultName}" autocomplete="off" style="font-family: 'Helvetica', Arial, sans-serif; font-weight: 500; font-size: 14px; border: none; outline: none; background: transparent; color: #111; padding: 0; width: 100%; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">
                            <div class="conn-info" style="display: none;">${infoString}</div>
                            <div class="conn-autocomplete" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 200px; flex-direction: column; max-height: 200px; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;"></div>
                        </div>
                        
                        <!-- Right side: Controls -->
                        <div style="display: flex; gap: 8px; align-items: center; justify-content: flex-end;">
                            <!-- Dropdown -->
                            <div style="position: relative; width: 110px;">
                                <div class="conn-type-display" style="font-size: 11px; font-weight: 500; color: #333; cursor: pointer; display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.04); padding: 6px 8px; border-radius: 6px;"><span>${getRelLabel(defaultType)}</span> <span style="font-size: 7px;">▼</span></div>
                                <div class="conn-type-dropdown" style="display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; z-index: 100; min-width: 120px; flex-direction: column; padding: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 5px;">
                                    <div class="conn-type-option" data-val="friend" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Friend</div>
                                    <div class="conn-type-option" data-val="acquaintance" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Acquaintance</div>
                                    <div class="conn-type-option" data-val="family_core" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Close)</div>
                                    <div class="conn-type-option" data-val="family_extended" style="padding: 8px 10px; font-size: 11px; cursor: pointer; color: #333; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(0,0,0,0.05)'" onmouseout="this.style.background='transparent'">Family (Ext)</div>
                                </div>
                                <input type="hidden" class="conn-type" value="${defaultType}">
                            </div>
                            
                            <!-- Slider -->
                            <div style="display: flex; align-items: center; gap: 5px; width: 70px;">
                                <input type="range" class="conn-strength light-slider" min="1" max="5" value="${defaultStrength}" style="flex: 1; min-width: 0;">
                                <span class="light-slider-val" style="font-family: 'Helvetica', Arial, sans-serif; font-size: 11px; font-weight: 500; color: #333; width: 10px; text-align: center;">${defaultStrength}</span>
                            </div>
                            
                            <!-- Remove Button -->
                            <button type="button" class="btn-remove-conn" style="background: transparent; border: none; color: #111; cursor: pointer; font-size: 16px; line-height: 1; padding: 0; margin-left: 0; opacity: 0.5; transition: 0.2s;" onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.5'">&times;</button>
                        </div>
                    </div>
                `;
            } else {
                div.style.background = 'transparent';
                div.style.border = '1px solid rgba(255,255,255,0.15)';
                div.style.borderRadius = '8px';
                div.style.padding = '30px';
                div.style.display = 'flex';
                div.style.justifyContent = 'space-between';
                div.style.alignItems = 'center';
                div.style.marginBottom = '15px';
                div.style.position = 'relative'; 

                div.innerHTML = `
                    <div style="flex: 1; display: flex; flex-direction: column; position: relative;">
                        <input type="text" class="conn-target" placeholder="Search Name..." value="${defaultName}" autocomplete="off" style="font-family: 'Helvetica', Arial, sans-serif; font-weight: 300; font-size: 16px; border: none; outline: none; background: transparent; color: #F5F5F5; padding: 0; margin-bottom: 4px; width: 100%;">
                        <div class="conn-info" style="font-family: 'Helvetica', Arial, sans-serif; font-size: 11px; color: rgba(255,255,255,0.5);">${infoString}</div>
                        <div class="conn-autocomplete" style="display: none; position: absolute; top: 100%; left: 0; background: rgba(10,10,10,0.95); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; z-index: 100; min-width: 200px; flex-direction: column; max-height: 400px; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-top: 5px;"></div>
                    </div>
                    
                    <div style="display: flex; gap: 30px; align-items: center;">
                        <div style="display: flex; flex-direction: column; position: relative;">
                            <div style="font-family: 'Helvetica', Arial, sans-serif; font-size: 12px; letter-spacing: 1px; color: rgba(255,255,255,0.5); text-transform: uppercase; margin-bottom: 4px;">Relationship</div>
                            <div class="conn-type-display" style="font-family: 'Helvetica', Arial, sans-serif; font-size: 16px; font-weight: 300; color: #F5F5F5; cursor: pointer; display: flex; justify-content: space-between; align-items: center; min-width: 100px;"><span>${getRelLabel(defaultType)}</span> <span style="font-size: 8px;">▼</span></div>
                            <div class="conn-type-dropdown" style="display: none; position: absolute; top: 100%; left: 0; background: rgba(10,10,10,0.95); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; z-index: 100; min-width: 160px; flex-direction: column; padding: 5px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-top: 5px;">
                                <div class="conn-type-option" data-val="friend" style="padding: 12px 15px; font-size: 13px; cursor: pointer; color: #F5F5F5; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">Friend</div>
                                <div class="conn-type-option" data-val="acquaintance" style="padding: 12px 15px; font-size: 13px; cursor: pointer; color: #F5F5F5; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">Acquaintance</div>
                                <div class="conn-type-option" data-val="family_core" style="padding: 12px 15px; font-size: 13px; cursor: pointer; color: #F5F5F5; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">Family (Close)</div>
                                <div class="conn-type-option" data-val="family_extended" style="padding: 12px 15px; font-size: 13px; cursor: pointer; color: #F5F5F5; transition: 0.2s; border-radius: 4px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">Family (Ext)</div>
                            </div>
                            <input type="hidden" class="conn-type" value="${defaultType}">
                        </div>
                        
                        <div style="width: 1px; height: 24px; background: rgba(255,255,255,0.15);"></div>

                        <div style="display: flex; flex-direction: column; position: relative;">
                            <div style="font-family: 'Helvetica', Arial, sans-serif; font-size: 12px; letter-spacing: 1px; color: rgba(255,255,255,0.5); text-transform: uppercase; margin-bottom: 4px;">Strength</div>
                            <div style="display: flex; align-items: center; width: 140px; height: 24px; position: relative;">
                                <input type="range" class="conn-strength strength-slider" min="1" max="5" value="${defaultStrength}" style="width: 100%;">
                                <div class="conn-strength-label" style="position: absolute; top: 20px; font-family: 'Helvetica', Arial, sans-serif; font-size: 10px; color: rgba(255,255,255,0.7); transform: translateX(-50%); pointer-events: none;">${defaultStrength}</div>
                            </div>
                        </div>
                        
                        <button type="button" class="btn-remove-conn" style="background: transparent; border: none; color: rgba(255,255,255,0.4); cursor: pointer; font-size: 18px; padding: 0 0 0 10px; line-height: 1; transition: 0.2s;">&times;</button>
                    </div>
                `;
            }
            
"""

new_html = html[:start_idx] + clean_code + html[end_idx:]

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Fixed UI styles successfully")
