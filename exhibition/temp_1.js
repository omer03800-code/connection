
                function switchEditTab(tabName) {
                    const detailsTab = document.getElementById('tab-edit-details');
                    const connsTab = document.getElementById('tab-edit-connections');
                    const detailsContent = document.getElementById('edit-person-form');
                    const connsContent = document.getElementById('edit-connections-tab-content');
                    
                    if (tabName === 'details') {
                        detailsTab.style.borderColor = '#000';
                        detailsTab.style.color = '#000';
                        connsTab.style.borderColor = 'transparent';
                        connsTab.style.color = '#999';
                        
                        detailsContent.style.display = 'flex';
                        connsContent.style.display = 'none';
                    } else {
                        connsTab.style.borderColor = '#000';
                        connsTab.style.color = '#000';
                        detailsTab.style.borderColor = 'transparent';
                        detailsTab.style.color = '#999';
                        
                        connsContent.style.display = 'flex';
                        detailsContent.style.display = 'none';
                    }
                }
            