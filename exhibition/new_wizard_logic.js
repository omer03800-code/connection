
        // --- NEW WIZARD LOGIC ---
        function goToWizardStep(step) {
            currentWizardStep = step;
            document.querySelectorAll('.wizard-step').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            
            const stepEl = document.getElementById(`wizard-step-${step}`);
            if (stepEl) {
                stepEl.style.display = 'block';
                void stepEl.offsetWidth; // reflow
                stepEl.classList.add('active');
            }
            
            const previewArea = document.getElementById('wizard-preview-area');
            if (step >= 4 && step <= 9) {
                previewArea.style.display = 'flex';
            } else {
                previewArea.style.display = 'none';
            }
        }

        function addNodeToPreview(label, value) {
            if (!value) return;
            const previewContainer = document.getElementById('live-network-preview');
            
            // Add line if not first node
            if (previewContainer.children.length > 0) {
                const line = document.createElement('div');
                line.className = 'preview-line';
                previewContainer.appendChild(line);
            }
            
            const node = document.createElement('div');
            node.className = 'preview-node';
            node.innerHTML = `
                <div class="preview-dot"></div>
                <div class="preview-text">${value}</div>
                <div style="font-size: 10px; color: rgba(245,245,245,0.4); text-transform: uppercase;">${label}</div>
            `;
            previewContainer.appendChild(node);
            
            // Scroll to bottom of preview
            const previewArea = document.getElementById('wizard-preview-area');
            previewArea.scrollTop = previewArea.scrollHeight;
        }

        // --- WIZARD EVENT LISTENERS ---
        document.getElementById('btn-wizard-next-1').addEventListener('click', () => {
            const nameInput = document.getElementById('f-name-initial').value.trim();
            if (!nameInput) {
                alert("Please enter a name first.");
                return;
            }
            
            document.getElementById('f-name').value = nameInput;
            document.getElementById('live-network-preview').innerHTML = ''; // reset preview
            addNodeToPreview('Name', nameInput);
            
            goToWizardStep(2);
            
            setTimeout(() => {
                const matchIndex = people.findIndex(p => p.name.toLowerCase() === nameInput.toLowerCase());
                if (matchIndex !== -1) {
                    const match = people[matchIndex];
                    document.getElementById('match-name').textContent = match.name;
                    document.getElementById('match-role').textContent = match.role || 'Unknown Role';
                    document.getElementById('match-city').textContent = match.city || 'Unknown City';
                    document.getElementById('btn-match-yes').dataset.matchIndex = matchIndex;
                    goToWizardStep(3);
                } else {
                    document.getElementById('form-mode').value = 'add';
                    goToWizardStep(4);
                }
            }, 1500);
        });

        document.getElementById('btn-match-yes').addEventListener('click', (e) => {
            const matchIndex = parseInt(e.currentTarget.dataset.matchIndex);
            closeModal();
            setTimeout(() => {
                selectNode(matchIndex, true);
            }, 300);
        });

        document.getElementById('btn-match-no').addEventListener('click', () => {
            document.getElementById('form-mode').value = 'add';
            document.getElementById('form-person-id').value = '';
            goToWizardStep(4);
        });

        document.getElementById('btn-wizard-back-4').addEventListener('click', () => goToWizardStep(1));
        document.getElementById('btn-wizard-next-4').addEventListener('click', () => {
            const birthYear = document.getElementById('f-birth-year').value;
            if (birthYear) {
                const currentYear = new Date().getFullYear();
                document.getElementById('f-age').value = currentYear - parseInt(birthYear);
            }
            const country = document.getElementById('f-country').value.trim().toLowerCase();
            const city = document.getElementById('f-city').value.trim();
            const originCity = document.getElementById('f-origin-city').value.trim();
            
            if (city) addNodeToPreview('City', city);
            if (originCity && originCity !== city) addNodeToPreview('Origin', originCity);
            
            // Conditional Israel logic
            if (country === 'israel' || country === 'il' || country === 'ישראל') {
                document.getElementById('israel-military-section').style.display = 'block';
                document.getElementById('israel-extra-section').style.display = 'block';
            } else {
                document.getElementById('israel-military-section').style.display = 'none';
                document.getElementById('israel-extra-section').style.display = 'none';
            }
            
            goToWizardStep(5);
        });

        document.getElementById('btn-wizard-back-5').addEventListener('click', () => goToWizardStep(4));
        document.getElementById('btn-wizard-next-5').addEventListener('click', () => {
            const role = document.getElementById('f-role').value.trim();
            const workplace = document.getElementById('f-workplace').value.trim();
            if (role) addNodeToPreview('Role', role);
            if (workplace) addNodeToPreview('Workplace', workplace);
            goToWizardStep(6);
        });

        document.getElementById('btn-wizard-back-6').addEventListener('click', () => goToWizardStep(5));
        document.getElementById('btn-wizard-next-6').addEventListener('click', () => {
            const highschool = document.getElementById('f-highschool').value.trim();
            const military = document.getElementById('f-military').value.trim();
            const education = document.getElementById('f-education').value.trim();
            const prevWork = document.getElementById('f-prev-work').value.trim();
            
            if (highschool) addNodeToPreview('High School', highschool);
            if (military) addNodeToPreview('Military', military);
            if (education) addNodeToPreview('Education', education);
            if (prevWork) addNodeToPreview('Previous Work', prevWork);
            
            goToWizardStep(7);
        });

        document.getElementById('btn-wizard-back-7').addEventListener('click', () => goToWizardStep(6));
        document.getElementById('btn-wizard-next-7').addEventListener('click', () => {
            const youth = document.getElementById('f-youth').value.trim();
            const community = document.getElementById('f-community').value.trim();
            const other = document.getElementById('f-other').value.trim();
            
            if (youth) addNodeToPreview('Youth Movement', youth);
            if (community) addNodeToPreview('Community', community);
            if (other) addNodeToPreview('Other', other);
            
            // Serialize chapters into tags and description
            let generatedTags = [];
            let generatedDesc = [];
            
            const addField = (val, prefix, isTag=true) => {
                if (val) {
                    if (isTag) generatedTags.push(`${prefix}:${val}`);
                    generatedDesc.push(`${prefix}: ${val}`);
                }
            };
            
            addField(document.getElementById('f-workplace').value.trim(), 'workplace');
            addField(document.getElementById('f-highschool').value.trim(), 'highschool');
            addField(document.getElementById('f-military').value.trim(), 'military');
            addField(document.getElementById('f-education').value.trim(), 'education');
            addField(document.getElementById('f-prev-work').value.trim(), 'prevwork');
            addField(document.getElementById('f-youth').value.trim(), 'youth');
            addField(document.getElementById('f-community').value.trim(), 'community');
            addField(document.getElementById('f-other').value.trim(), 'other');
            
            document.getElementById('f-tags').value = generatedTags.join(', ');
            document.getElementById('f-desc').value = generatedDesc.join('\n');
            
            // Generate Recommendations based on these new tags
            generateRecommendations();
            
            goToWizardStep(8);
        });

        document.getElementById('btn-wizard-back-8').addEventListener('click', () => goToWizardStep(7));
        document.getElementById('btn-wizard-next-8').addEventListener('click', () => {
            goToWizardStep(9);
        });

        document.getElementById('btn-wizard-back-9').addEventListener('click', () => goToWizardStep(8));
        document.getElementById('btn-wizard-next-9').addEventListener('click', () => {
            goToWizardStep(10);
            
            setTimeout(() => {
                // Trigger form submission
                const addForm = document.getElementById('add-form');
                if (addForm) {
                    addForm.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
                }
            }, 1500);
        });

        // --- AUTOCOMPLETE LOGIC ---
        function setupAutocomplete(inputId, prefix) {
            const input = document.getElementById(inputId);
            const dropdown = document.getElementById('dropdown-' + inputId);
            const stats = document.getElementById('stats-' + inputId);
            if (!input || !dropdown || !stats) return;

            input.addEventListener('input', () => {
                const val = input.value.trim().toLowerCase();
                dropdown.innerHTML = '';
                stats.innerHTML = '';
                
                if (!val) {
                    dropdown.style.display = 'none';
                    return;
                }
                
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
                });
                
                // Filter and sort
                const suggestions = Object.keys(counts)
                    .filter(k => k.toLowerCase().includes(val))
                    .sort((a, b) => counts[b] - counts[a])
                    .slice(0, 5);
                
                if (suggestions.length > 0) {
                    suggestions.forEach(s => {
                        const div = document.createElement('div');
                        div.className = 'autocomplete-item';
                        div.innerHTML = `<span>${s}</span> <span class="autocomplete-count">${counts[s]} people</span>`;
                        div.onclick = () => {
                            input.value = s;
                            dropdown.style.display = 'none';
                            stats.innerHTML = `${counts[s]} people in the network are connected to this.`;
                        };
                        dropdown.appendChild(div);
                    });
                    dropdown.style.display = 'block';
                } else {
                    dropdown.style.display = 'none';
                    stats.innerHTML = `You are the first one in the network to add this!`;
                }
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', (e) => {
                if (e.target !== input && e.target !== dropdown) {
                    dropdown.style.display = 'none';
                }
            });
        }

        // Initialize autocompletes
        setupAutocomplete('f-city', 'city');
        setupAutocomplete('f-origin-city', 'city');
        setupAutocomplete('f-role', 'role');
        setupAutocomplete('f-workplace', 'workplace');
        setupAutocomplete('f-highschool', 'highschool');
        setupAutocomplete('f-military', 'military');
        setupAutocomplete('f-education', 'education');
        setupAutocomplete('f-prev-work', 'prevwork');
        setupAutocomplete('f-youth', 'youth');
        setupAutocomplete('f-community', 'community');
        setupAutocomplete('f-other', 'other');

