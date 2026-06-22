import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace Step 6 and Step 7 with Unified Step 6
pattern_html = r'<!-- STEP 6 LIFE CHAPTERS -->.*?<!-- STEP 8 SHARED PATHS \(Suggested Connections\) -->'
replacement_html = """<!-- STEP 6 LIFE CHAPTERS (Unified) -->
                <div id="wizard-step-6" class="wizard-step">
                    <h2 class="modal-title">Life Chapters</h2>
                    <p class="modal-subtitle">What else shaped their path? (Optional)</p>
                    
                    <div id="life-chapters-container"></div>
                    
                    <div style="margin-bottom: 30px;">
                        <select id="chapter-selector" class="editorial-input" style="width: 100%; border: 1px dashed rgba(245,245,245,0.3); background: transparent; color: inherit; border-radius: 8px; padding: 10px; cursor: pointer; text-transform: uppercase; font-size: 11px; letter-spacing: 1px;">
                            <option value="" disabled selected>[ + ADD CHAPTER ]</option>
                            <option value="highschool" style="color: black;">High School</option>
                            <option value="military" class="israel-only" style="color: black;">Military Service</option>
                            <option value="education" style="color: black;">Higher Education</option>
                            <option value="prev-work" style="color: black;">Previous Work History</option>
                            <option value="youth" class="israel-only" style="color: black;">Mechina / Gap Year / Youth Movement</option>
                            <option value="community" style="color: black;">Community / Volunteer Work</option>
                            <option value="other" style="color: black;">Other</option>
                        </select>
                    </div>

                    <div id="hidden-chapters" style="display: none;">
                        <div class="chapter-block autocomplete-wrapper" id="block-highschool">
                            <label class="editorial-label" style="display:flex; justify-content:space-between;">High School <span class="remove-chapter" data-id="highschool" style="cursor: pointer; opacity: 0.5;">&times; Remove</span></label>
                            <input type="text" id="f-highschool" class="editorial-input auto-highschool" placeholder="School Name" autocomplete="off">
                            <div class="autocomplete-dropdown" id="dropdown-f-highschool"></div>
                        </div>
                        <div class="chapter-block autocomplete-wrapper" id="block-military">
                            <label class="editorial-label" style="display:flex; justify-content:space-between;">Military Service <span class="remove-chapter" data-id="military" style="cursor: pointer; opacity: 0.5;">&times; Remove</span></label>
                            <input type="text" id="f-military" class="editorial-input auto-military" placeholder="Unit, Base, or Role" autocomplete="off">
                            <div class="autocomplete-dropdown" id="dropdown-f-military"></div>
                        </div>
                        <div class="chapter-block autocomplete-wrapper" id="block-education">
                            <label class="editorial-label" style="display:flex; justify-content:space-between;">Higher Education <span class="remove-chapter" data-id="education" style="cursor: pointer; opacity: 0.5;">&times; Remove</span></label>
                            <input type="text" id="f-education" class="editorial-input auto-education" placeholder="University, College, Course" autocomplete="off">
                            <div class="autocomplete-dropdown" id="dropdown-f-education"></div>
                        </div>
                        <div class="chapter-block autocomplete-wrapper" id="block-prev-work">
                            <label class="editorial-label" style="display:flex; justify-content:space-between;">Previous Work History <span class="remove-chapter" data-id="prev-work" style="cursor: pointer; opacity: 0.5;">&times; Remove</span></label>
                            <input type="text" id="f-prev-work" class="editorial-input auto-work" placeholder="Previous Company" autocomplete="off">
                            <div class="autocomplete-dropdown" id="dropdown-f-prev-work"></div>
                        </div>
                        <div class="chapter-block autocomplete-wrapper" id="block-youth">
                            <label class="editorial-label" style="display:flex; justify-content:space-between;">Mechina / Youth Movement <span class="remove-chapter" data-id="youth" style="cursor: pointer; opacity: 0.5;">&times; Remove</span></label>
                            <input type="text" id="f-youth" class="editorial-input auto-youth" placeholder="Movement or Program" autocomplete="off">
                            <div class="autocomplete-dropdown" id="dropdown-f-youth"></div>
                        </div>
                        <div class="chapter-block autocomplete-wrapper" id="block-community">
                            <label class="editorial-label" style="display:flex; justify-content:space-between;">Community / Volunteer Work <span class="remove-chapter" data-id="community" style="cursor: pointer; opacity: 0.5;">&times; Remove</span></label>
                            <input type="text" id="f-community" class="editorial-input auto-community" placeholder="Organization or Community" autocomplete="off">
                            <div class="autocomplete-dropdown" id="dropdown-f-community"></div>
                        </div>
                        <div class="chapter-block autocomplete-wrapper" id="block-other">
                            <label class="editorial-label" style="display:flex; justify-content:space-between;">Other Chapter <span class="remove-chapter" data-id="other" style="cursor: pointer; opacity: 0.5;">&times; Remove</span></label>
                            <input type="text" id="f-other" class="editorial-input auto-other" placeholder="Anything else?" autocomplete="off">
                            <div class="autocomplete-dropdown" id="dropdown-f-other"></div>
                        </div>
                    </div>

                    <div class="wizard-buttons">
                        <button type="button" class="info-action-btn" id="btn-wizard-back-6">[ BACK ]</button>
                        <button type="button" class="info-action-btn" id="btn-wizard-next-6">[ NEXT ]</button>
                    </div>
                </div>

                <!-- STEP 8 SHARED PATHS (Suggested Connections) -->"""

html = re.sub(pattern_html, replacement_html, html, flags=re.DOTALL)

# 2. Update the JS logic for Step 6 and remove Step 7
pattern_js = r"document\.getElementById\('btn-wizard-back-6'\)\.addEventListener\('click', \(\) => goToWizardStep\(5\)\);.*?document\.getElementById\('btn-wizard-back-8'\)\.addEventListener\('click', \(\) => goToWizardStep\(7\)\);"
replacement_js = """document.getElementById('btn-wizard-back-6').addEventListener('click', () => goToWizardStep(5));
        document.getElementById('btn-wizard-next-6').addEventListener('click', () => {
            const highschool = document.getElementById('f-highschool').value.trim();
            const military = document.getElementById('f-military').value.trim();
            const education = document.getElementById('f-education').value.trim();
            const prevWork = document.getElementById('f-prev-work').value.trim();
            const youth = document.getElementById('f-youth').value.trim();
            const community = document.getElementById('f-community').value.trim();
            const other = document.getElementById('f-other').value.trim();
            
            if (highschool && document.getElementById('block-highschool').parentElement.id !== 'hidden-chapters') addNodeToOrganicPreview('High School', highschool);
            if (military && document.getElementById('block-military').parentElement.id !== 'hidden-chapters') addNodeToOrganicPreview('Military', military);
            if (education && document.getElementById('block-education').parentElement.id !== 'hidden-chapters') addNodeToOrganicPreview('Education', education);
            if (prevWork && document.getElementById('block-prev-work').parentElement.id !== 'hidden-chapters') addNodeToOrganicPreview('Previous Work', prevWork);
            if (youth && document.getElementById('block-youth').parentElement.id !== 'hidden-chapters') addNodeToOrganicPreview('Youth Movement', youth);
            if (community && document.getElementById('block-community').parentElement.id !== 'hidden-chapters') addNodeToOrganicPreview('Community', community);
            if (other && document.getElementById('block-other').parentElement.id !== 'hidden-chapters') addNodeToOrganicPreview('Other', other);
            
            generateRecommendations();
            goToWizardStep(8);
        });

        // Initialize chapter selector
        document.getElementById('chapter-selector').addEventListener('change', function(e) {
            const val = e.target.value;
            if (!val) return;
            const block = document.getElementById('block-' + val);
            if (block) {
                document.getElementById('life-chapters-container').appendChild(block);
            }
            e.target.value = ''; // Reset selector
            
            // Remove the option so it can't be added twice
            Array.from(e.target.options).forEach(opt => {
                if(opt.value === val) opt.style.display = 'none';
            });
        });

        // Handle remove chapter clicks
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-chapter')) {
                const id = e.target.dataset.id;
                const block = document.getElementById('block-' + id);
                if (block) {
                    document.getElementById('hidden-chapters').appendChild(block);
                    document.getElementById('f-' + id).value = ''; // clear value
                }
                // Restore option
                const select = document.getElementById('chapter-selector');
                Array.from(select.options).forEach(opt => {
                    if(opt.value === id) opt.style.display = 'block';
                });
            }
        });

        document.getElementById('btn-wizard-back-8').addEventListener('click', () => goToWizardStep(6));"""

html = re.sub(pattern_js, replacement_js, html, flags=re.DOTALL)

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
