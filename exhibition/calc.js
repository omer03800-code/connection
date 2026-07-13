        function calculateMatchScore(p1, p2) {
            const ignoreCities = ['tel aviv', 'jerusalem', 'haifa', 'ramat gan', 'תל אביב', 'ירושלים', 'חיפה', 'רמת גן'];
            const synonymGroups = [
                { type: 'degree', words: ['design', 'visual communication', 'designer', 'ux', 'ui', 'עיצוב', 'תקשורת חזותית', 'מעצבת', 'מעצב'] },
                { type: 'uni', words: ['haifa university', 'university of haifa', 'wizo', 'אוניברסיטת חיפה', 'ויצו חיפה'] },
                { type: 'city', words: ['ilaniya', 'ilania', 'אילניה', 'מושב אילניה'] },
                { type: 'city', words: ['bat hefer', 'בת חפר'] },
                { type: 'city', words: ['akko', 'acre', 'עכו'] },
                { type: 'city', words: ['tzfat', 'safed', 'צפת'] },
                { type: 'city', words: ['pardes hanna', 'pardes hanna karkur', 'pardes hanna-karkur', 'פרדס חנה', 'פרדס חנה כרכור'] },
                { type: 'city', words: ['zikhron yaakov', 'zikhron ya\'akov', 'זכרון יעקב'] },
                { type: 'degree', words: ['computer science', 'מדעי המחשב', 'cs', 'software engineering', 'הנדסת תוכנה'] },
                { type: 'degree', words: ['electrical engineering', 'הנדסת חשמל', 'ee'] },
                { type: 'degree', words: ['industrial engineering', 'הנדסת תעשייה וניהול', 'תעשייה וניהול'] },
                { type: 'degree', words: ['business administration', 'מנהל עסקים'] },
                { type: 'degree', words: ['economics', 'כלכלה'] },
                { type: 'degree', words: ['psychology', 'פסיכולוגיה'] },
                { type: 'degree', words: ['law', 'משפטים', 'עריכת דין'] },
                { type: 'degree', words: ['medicine', 'רפואה'] },
                { type: 'degree', words: ['nursing', 'סיעוד'] },
                { type: 'degree', words: ['education', 'חינוך', 'הוראה'] },
                { type: 'degree', words: ['accounting', 'ראיית חשבון', 'חשבונאות'] },
                { type: 'degree', words: ['architecture', 'אדריכלות', 'ארכיטקטורה'] },
                { type: 'degree', words: ['marketing', 'שיווק', 'communications', 'תקשורת'] },
                { type: 'degree', words: ['data science', 'מדע הנתונים', 'דאטה סיינס'] },
                { type: 'degree', words: ['political science', 'מדעי המדינה'] },
                { type: 'degree', words: ['social work', 'עבודה סוציאלית'] },
                { type: 'degree', words: ['biology', 'ביולוגיה'] },
                { type: 'degree', words: ['mechanical engineering', 'הנדסת מכונות'] },
                { type: 'uni', words: ['tel aviv university', 'tau', 'אוניברסיטת תל אביב'] },
                { type: 'uni', words: ['hebrew university', 'huji', 'האוניברסיטה העברית'] },
                { type: 'uni', words: ['technion', 'הטכניון'] },
                { type: 'uni', words: ['weizmann', 'weizmann institute of science', 'מכון ויצמן'] },
                { type: 'uni', words: ['ben gurion university', 'bgu', 'אוניברסיטת בן גוריון', 'בן גוריון'] },
                { type: 'uni', words: ['bar ilan university', 'biu', 'בר אילן', 'bar ilan'] },
                { type: 'uni', words: ['reichman university', 'idc', 'רייכמן', 'הבינתחומי'] },
                { type: 'uni', words: ['shenkar', 'שנקר'] },
                { type: 'uni', words: ['bezalel', 'בצלאל', 'bezalel academy'] },
                { type: 'uni', words: ['colman', 'המכללה למינהל', 'מכללה למנהל', 'the college of management'] },
                { type: 'uni', words: ['open university', 'האוניברסיטה הפתוחה'] },
                { type: 'uni', words: ['hit', 'holon institute of technology', 'מכון טכנולוגי חולון'] },
                { type: 'army_unit', words: ['operations room controller', 'sambatzit', 'סמבצית'] },
                { type: 'company', words: ['google'] }, { type: 'company', words: ['microsoft'] }, { type: 'company', words: ['apple'] }, { type: 'company', words: ['amazon'] }, { type: 'company', words: ['nvidia'] }, { type: 'company', words: ['intel'] }, { type: 'company', words: ['meta', 'facebook'] }, { type: 'company', words: ['ibm'] }, { type: 'company', words: ['salesforce'] }, { type: 'company', words: ['monday.com', 'monday'] }, { type: 'company', words: ['wix'] }, { type: 'company', words: ['fiverr'] }, { type: 'company', words: ['check point', 'checkpoint'] }, { type: 'company', words: ['cyberark'] }, { type: 'company', words: ['nice'] }, { type: 'company', words: ['amdocs'] }, { type: 'company', words: ['playtika'] }, { type: 'company', words: ['etoro'] }, { type: 'company', words: ['taboola'] }, { type: 'company', words: ['outbrain'] },
                { type: 'army_unit', words: ['golani'] }, { type: 'army_unit', words: ['givati'] }, { type: 'army_unit', words: ['nahal'] }, { type: 'army_unit', words: ['paratroopers', 'tzanhanim'] }, { type: 'army_unit', words: ['kfir'] }, { type: 'army_unit', words: ['armored corps', 'shiryon'] }, { type: 'army_unit', words: ['artillery', 'totchanim'] }, { type: 'army_unit', words: ['combat engineering', 'handasa kravit'] }, { type: 'army_unit', words: ['air force', 'heil haavir'] }, { type: 'army_unit', words: ['navy', 'heil hayam'] }, { type: 'army_unit', words: ['home front command', 'pikud haoref'] }, { type: 'army_unit', words: ['border police', 'magav'] }, { type: 'army_unit', words: ['intelligence', 'aman'] }, { type: 'army_unit', words: ['sayeret matkal', 'general staff reconnaissance'] }, { type: 'army_unit', words: ['shayetet 13', 'naval commandos'] }, { type: 'army_unit', words: ['shaldag', 'air force commandos'] }, { type: 'army_unit', words: ['maglan', 'special forces'] }, { type: 'army_unit', words: ['duvdevan', 'undercover unit'] }, { type: 'army_unit', words: ['egoz', 'reconnaissance unit'] }, { type: 'army_unit', words: ['yahalom', 'combat engineering special forces'] }, { type: 'army_unit', words: ['oketz', 'k9 unit'] }, { type: 'army_unit', words: ['unit 669', 'combat search and rescue'] }, { type: 'army_unit', words: ['unit 8200', '8200', 'signals intelligence'] }, { type: 'army_unit', words: ['lotar', 'counter-terror'] },
                { type: 'army_base', words: ['bahad 1'] }, { type: 'army_base', words: ['bahad 7'] }, { type: 'army_base', words: ['bahad 12'] }, { type: 'army_base', words: ['glilot'] }, { type: 'army_base', words: ['kirya'] }, { type: 'army_base', words: ['tel hashomer'] }, { type: 'army_base', words: ['ir habahadim'] }, { type: 'army_base', words: ['tzrifin'] }, { type: 'army_base', words: ['nevatim'] }, { type: 'army_base', words: ['hatzerim'] }, { type: 'army_base', words: ['ramat david'] }, { type: 'army_base', words: ['palmachim'] }, { type: 'army_base', words: ['ramon'] }, { type: 'army_base', words: ['ovda'] }, { type: 'army_base', words: ['ze\'elim', 'zeelim'] }, { type: 'army_base', words: ['re\'im', 'reim'] }, { type: 'army_base', words: ['urim'] }, { type: 'army_base', words: ['nafah'] }, { type: 'army_base', words: ['saar 474'] }, { type: 'army_base', words: ['barak 188'] }, { type: 'army_base', words: ['golani 1'] }, { type: 'army_base', words: ['givati 84'] }, { type: 'army_base', words: ['nahal 933'] }, { type: 'army_base', words: ['tzanhanim 35'] }, { type: 'army_base', words: ['kfir 900'] }, { type: 'army_base', words: ['harel 10'] }, { type: 'army_base', words: ['alexandroni 3'] }, { type: 'army_base', words: ['carmeli 2'] },
                { type: 'high_school', words: ['reali'] }, { type: 'high_school', words: ['alliance'] }, { type: 'high_school', words: ['gymnasia herzliya', 'gymnasia'] }, { type: 'high_school', words: ['leo baeck'] }, { type: 'high_school', words: ['thelma yellin'] }, { type: 'high_school', words: ['kfar hayarok'] }, { type: 'high_school', words: ['mosinson'] }, { type: 'high_school', words: ['hadassim'] }, { type: 'high_school', words: ['ben shemen'] }, { type: 'high_school', words: ['kadoorie'] }, { type: 'high_school', words: ['wizo nahalal'] }, { type: 'high_school', words: ['shevach mofet'] }, { type: 'high_school', words: ['boyar'] }, { type: 'high_school', words: ['leyada'] }, { type: 'high_school', words: ['harel'] }, { type: 'high_school', words: ['ort singalovski'] }, { type: 'high_school', words: ['ort bialik'] }, { type: 'high_school', words: ['ort motzkin'] }, { type: 'high_school', words: ['ort ginzburg'] }, { type: 'high_school', words: ['ort'] }, { type: 'high_school', words: ['amal'] }, { type: 'high_school', words: ['atid'] }, { type: 'high_school', words: ['darca'] }, { type: 'high_school', words: ['branco weiss'] }, { type: 'high_school', words: ['ironi alef'] }, { type: 'high_school', words: ['ironi bet'] }, { type: 'high_school', words: ['ironi gimel'] }, { type: 'high_school', words: ['ironi dalet'] }, { type: 'high_school', words: ['ironi hey'] }, { type: 'high_school', words: ['ironi vav'] }, { type: 'high_school', words: ['makif alef'] }, { type: 'high_school', words: ['makif bet'] }, { type: 'high_school', words: ['makif gimel'] }, { type: 'high_school', words: ['makif dalet'] }, { type: 'high_school', words: ['makif hey'] }, { type: 'high_school', words: ['makif vav'] }, { type: 'high_school', words: ['makif zayin'] }, { type: 'high_school', words: ['makif het'] }, { type: 'high_school', words: ['rabin'] }, { type: 'high_school', words: ['begin'] }, { type: 'high_school', words: ['blich', 'בליך'] }, { type: 'high_school', words: ['misgav', 'משגב'] }, { type: 'high_school', words: ['yifat', 'יפעת'] },
                { type: 'mechina', words: ['derech eretz - nitzana', 'nitzana'] }, { type: 'mechina', words: ['derech eretz - kmehin', 'kmehin'] }, { type: 'mechina', words: ['derech eretz - ein yahav', 'ein yahav'] }, { type: 'mechina', words: ['derech eretz - ashalim', 'ashalim'] }, { type: 'mechina', words: ['bnei david'] }, { type: 'mechina', words: ['ein prat'] }, { type: 'mechina', words: ['nachshon'] }, { type: 'mechina', words: ['mechinat rabin', 'rabin'] }, { type: 'mechina', words: ['gal'] }, { type: 'mechina', words: ['maayan baruch'] }, { type: 'mechina', words: ['tavor'] }, { type: 'mechina', words: ['lachish'] }, { type: 'mechina', words: ['arava'] }, { type: 'mechina', words: ['yachad'] }, { type: 'mechina', words: ['hanegev'] }, { type: 'mechina', words: ['aderet'] }, { type: 'mechina', words: ['keshet yehuda'] }, { type: 'mechina', words: ['haruach haisraelit'] }, { type: 'mechina', words: ['meitar'] }, { type: 'mechina', words: ['kol ami'] }
            ];
            const genericRoles = ['softwareengineer', 'fullstackdeveloper', 'frontenddeveloper', 'backenddeveloper', 'mobiledeveloper', 'iosdeveloper', 'androiddeveloper', 'webdeveloper', 'gamedeveloper', 'devopsengineer', 'sitelieliabilityengineer', 'sre', 'cloudengineer', 'cloudarchitect', 'solutionsarchitect', 'dataengineer', 'dataanalyst', 'datascientist', 'machinelearningengineer', 'aiengineer', 'airesearcher', 'promptengineer', 'cybersecurityanalyst', 'cybersecurityengineer', 'informationsecuritymanager', 'penetrationtester', 'socanalyst', 'qaengineer', 'automationengineer', 'testengineer', 'productmanager', 'technicalproductmanager', 'projectmanager', 'programmanager', 'scrummaster', 'businessanalyst', 'systemsanalyst', 'uxdesigner', 'uidesigner', 'uxresearcher', 'productdesigner', 'servicedesigner', 'interactiondesigner', 'technicalwriter', 'solutionsconsultant', 'customersuccessmanager', 'technicalsupportengineer', 'salesengineer', 'presalesengineer', 'itmanager', 'itadministrator', 'databaseadministrator', 'dba', 'networkengineer', 'embeddedsystemsengineer', 'hardwareengineer', 'electronicsengineer', 'roboticsengineer', 'computervisionengineer', 'blockchaindeveloper', 'arvrdeveloper', 'marketingmanager', 'digitalmarketingmanager', 'brandmanager', 'marketingdirector', 'chiefmarketingofficer', 'cmo', 'performancemarketingmanager', 'growthmarketingmanager', 'productmarketingmanager', 'contentmarketingmanager', 'socialmediamanager', 'communitymanager', 'influencermarketingmanager', 'emailmarketingspecialist', 'seospecialist', 'semspecialist', 'ppcspecialist', 'marketingspecialist', 'marketingcoordinator', 'marketinganalyst', 'marketresearchanalyst', 'brandstrategist', 'creativestrategist', 'communicationsmanager', 'publicrelationsmanager', 'prmanager', 'prspecialist', 'mediaplanner', 'mediabuyer', 'campaignmanager', 'advertisingmanager', 'copywriter', 'contentcreator', 'contentmanager', 'contentstrategist', 'creativedirector', 'artdirector', 'graphicdesigner', 'uxwriter', 'crmmanager', 'partnershipmanager', 'businessdevelopmentmanager', 'eventmanager', 'eventproducer', 'ecommercemanager', 'affiliatemarketingmanager', 'influencerrelationsmanager', 'marketingconsultant', 'freelancer', 'welfarenco', 'mashakittash', 'combatsoldier', 'lochem', 'lochemet', 'educationnco', 'mashakitchinuch', 'operationsroomcontroller', 'sambatzit', 'commander', 'mefaked', 'mefakedet', 'intelligenceanalyst', 'modiin', 'infantryinstructor', 'madrichatchir', 'combatinstructor', 'madrichatkrav', 'traininginstructor', 'madricha', 'operationsnco', 'mashakmivtzaim', 'humanresourcesnco', 'mashakitkoachadam', 'hightech', 'hitech', 'high-tech', 'hi-tech', 'tech', 'student', 'manager', 'friend', 'friends', 'family', 'colleague', 'partner', 'ex', 'designer', 'insurance'];
            
            const p1Tags = p1.tags ? (Array.isArray(p1.tags) ? p1.tags.map(t=>t.trim().toLowerCase()) : p1.tags.split(',').map(t=>t.trim().toLowerCase()).filter(Boolean)) : [];
            const p1TagsCleaned = p1Tags.map(t => t.replace(/.*?:/, '').replace(/^#/, ''));
            const p1Text = ' ' + [(p1.city||'').toLowerCase(), (p1.originCity||'').toLowerCase(), (p1.role||'').toLowerCase(), (p1.description||'').toLowerCase(), ...p1TagsCleaned].join(' ').replace(/[,.!]/g, ' ') + ' ';
            const p1Years = p1Tags.map(t => t.replace(/^#/, '')).filter(t => /^(19|20)\d{2}$/.test(t));
            const p1Age = p1.age ? parseInt(p1.age) : null;
            let p1CityLower = p1.city ? p1.city.toLowerCase() : '';
            const p1RoleLower = p1.role ? p1.role.toLowerCase() : '';
            
            let activeGroups = [];
            synonymGroups.forEach((group, idx) => {
                if (group.words.some(word => p1Text.includes(' ' + word + ' '))) {
                    activeGroups.push({ idx: idx, type: group.type });
                }
            });
            
            let score = 0;
            
            const p2Tags = p2.tags ? (Array.isArray(p2.tags) ? p2.tags : p2.tags.split(',').map(t=>t.trim().toLowerCase()).filter(Boolean)) : [];
            const p2TagsCleaned = p2Tags.map(t => t.replace(/.*?:/, '').replace(/^#/, ''));
            const p2Text = ' ' + [(p2.city||'').toLowerCase(), (p2.role||'').toLowerCase(), ...p2TagsCleaned].join(' ').replace(/[,.!]/g, ' ') + ' ';
            const p2Years = p2Tags.map(t => t.replace(/^#/, '')).filter(t => /^(19|20)\d{2}$/.test(t));
            const p2Age = p2.age ? parseInt(p2.age) : null;
            let p2CityLower = p2.city ? p2.city.toLowerCase() : '';
            p1Tags.forEach(t => { if(t.startsWith('city:')) p1CityLower += " " + t.substring(5).toLowerCase(); });
            p2Tags.forEach(t => { if(t.startsWith('city:')) p2CityLower += " " + t.substring(5).toLowerCase(); });
            const p2RoleLower = p2.role ? p2.role.toLowerCase() : '';
            
            let shared = { uni: 0, degree: 0, company: 0, city: 0, army_unit: 0, army_base: 0, high_school: 0, mechina: 0 };
            let genericSchoolMatch = false;
            let sharedStrings = [];
            
            activeGroups.forEach(ag => {
                if (synonymGroups[ag.idx].words.some(word => p2Text.includes(' ' + word + ' '))) {
                    shared[ag.type]++;
                    sharedStrings.push(synonymGroups[ag.idx].words[0]);
                    if (ag.type === 'high_school') {
                        const schoolName = synonymGroups[ag.idx].words[0];
                        if (schoolName.includes('ironi') || schoolName.includes('makif') || ['ort', 'amal', 'atid', 'darca', 'rabin', 'begin'].includes(schoolName)) {
                            genericSchoolMatch = true;
                        }
                    }
                }
            });
            
            const sharedYear = p1Years.some(y => p2Years.includes(y));
            const ageDiff = (p1Age !== null && p2Age !== null && !isNaN(p1Age) && !isNaN(p2Age)) ? Math.abs(p1Age - p2Age) : null;
            const isSimilarAge = (ageDiff !== null && ageDiff <= 3);
            const isSameCity = (p1CityLower && p2CityLower && (p2CityLower.includes(p1CityLower) || p1CityLower.includes(p2CityLower)));
            
            if (shared.company > 0) score += 35;
            if (shared.city > 0) score += 5; // Reduced from 35 to avoid massive grouping for big cities
            
            if (shared.high_school > 0) {
                if (genericSchoolMatch && !isSameCity) {
                    // Generic school requires same city to give points
                } else if (isSimilarAge) {
                    score += 45;
                }
            }
            if (shared.mechina > 0 && isSimilarAge) score += 45;
            if (shared.army_unit > 0 && isSimilarAge) score += 15;
            if (shared.army_base > 0 && isSimilarAge) score += 30;
            
            // Require BOTH university and specific degree/department to give significant points
            if (shared.uni > 0 && shared.degree > 0 && sharedYear) score += 45;
            else if (shared.uni > 0 && shared.degree > 0) score += 35;
            else if (shared.uni > 0 && sharedYear) score += 5; // Negligible
            else if (shared.uni > 0) score += 2; // Negligible
            
            if (shared.degree > 0 && shared.uni === 0) score += 2; // Generic profession alone gives negligible points
            
            if (p1CityLower && p2CityLower) {
                const cityAliases = {
                    'אילניה': ['ilaniya', 'ilania', 'אילניה'],
                    'איניה': ['ilaniya', 'ilania', 'אילניה', 'איניה'],
                    'moshav ilaniya': ['אילניה', 'ilania', 'ilaniya', 'moshav ilania', 'moshav ilaniya', 'מושב אילניה'],
                    'מושב אילניה': ['ilaniya', 'ilania', 'moshav ilania', 'moshav ilaniya', 'אילניה'],
                    'haifa': ['חיפה', 'haifa'],
                    'חיפה': ['haifa', 'חיפה'],
                    'tel aviv': ['תל אביב', 'tel aviv', 'tel-aviv'],
                    'tel aviv': ['tel aviv', 'tel-aviv', 'tlv', 'tel aviv-yafo', 'תל אביב', 'תל-אביב', 'תל אביב-יפו'],
                    'tel-aviv': ['tel aviv', 'tel-aviv', 'tlv', 'tel aviv-yafo', 'תל אביב', 'תל-אביב', 'תל אביב-יפו'],
                    'תל אביב': ['tel aviv', 'tel-aviv', 'tlv', 'tel aviv-yafo', 'תל אביב', 'תל-אביב', 'תל אביב-יפו'],
                    'rishon lezion': ['rishon', 'rishon lezion', 'ראשון לציון', 'ראשון'],
                    'ראשון לציון': ['rishon', 'rishon lezion', 'ראשון לציון', 'ראשון'],
                    'petah tikva': ['petah tikva', 'פתח תקווה', 'פ"ת', 'פתח-תקווה'],
                    'פתח תקווה': ['petah tikva', 'פתח תקווה', 'פ"ת', 'פתח-תקווה'],
                    'jerusalem': ['jerusalem', 'ירושלים'],
                    'ירושלים': ['jerusalem', 'ירושלים'],
                    'kfar saba': ['kfar saba', 'כפר סבא', 'כפ"ס'],
                    'כפר סבא': ['kfar saba', 'כפר סבא', 'כפ"ס'],
                    'beit keshet': ['beit keshet', 'בית קשת'],
                    'בית קשת': ['beit keshet', 'בית קשת'],
                    'gan shmuel': ['gan shmuel', 'גן שמואל'],
                    'גן שמואל': ['gan shmuel', 'גן שמואל']
                };

                let p1Vals = p1CityLower.split(/\||\/|,|\s-\s|—|\n|\sand\s|\s&\s/i).map(s => s.trim()).filter(Boolean);
                let p2Vals = p2CityLower.split(/\||\/|,|\s-\s|—|\n|\sand\s|\s&\s/i).map(s => s.trim()).filter(Boolean);
                
                let expandedP1Vals = [...p1Vals];
                let expandedP2Vals = [...p2Vals];

                Object.keys(cityAliases).forEach(k => {
                    if (p1Vals.some(v => v.includes(k))) expandedP1Vals = expandedP1Vals.concat(cityAliases[k]);
                    if (p2Vals.some(v => v.includes(k))) expandedP2Vals = expandedP2Vals.concat(cityAliases[k]);
                });

                let matchFound = false;
                let matchedVal = '';
                expandedP1Vals.forEach(v1 => {
                    expandedP2Vals.forEach(v2 => {
                        if (v1 === v2 || v1.includes(' ' + v2 + ' ') || v1.startsWith(v2 + ' ') || v1.endsWith(' ' + v2) || 
                            v2.includes(' ' + v1 + ' ') || v2.startsWith(v1 + ' ') || v2.endsWith(' ' + v1)) {
                            matchFound = true;
                            matchedVal = v1.length < v2.length ? v1 : v2; // take the shorter one as the match core
                        }
                    });
                });
                
                if (matchFound) {
                    const shouldIgnore = ignoreCities.some(c => matchedVal.includes(c));
                    if (!shouldIgnore) {
                        score += 15;
                        sharedStrings.push(matchedVal);
                    }
                    // Large cities are ignored completely, regardless of age
                }
            }
            if (p1RoleLower && p2RoleLower) {
                if (p2RoleLower === p1RoleLower) score += 5;
                else if (p2RoleLower.includes(p1RoleLower) || p1RoleLower.includes(p2RoleLower)) score += 2;
                else {
                    const fWords = p1RoleLower.split(/\s+/).filter(w => w.length > 2);
                    const pWords = p2RoleLower.split(/\s+/).filter(w => w.length > 2);
                    fWords.forEach(fw => {
                        if (pWords.some(pw => pw.includes(fw) || fw.includes(pw))) score += 1;
                    });
                }
            }
            p2Tags.forEach(t => {
                const cleanTag = t.replace(/^#/, '');
                const normTagFull = cleanTag.toLowerCase();
                const valTag = normTagFull.includes(':') ? normTagFull.split(':')[1].trim() : normTagFull.trim();
                const normTagStripped = valTag.replace(/\s+/g, '');
                
                const match = p1Tags.find(p1t => {
                    const cleanP1 = p1t.replace(/^#/, '');
                    const normP1Full = cleanP1.toLowerCase();
                    const valP1 = normP1Full.includes(':') ? normP1Full.split(':')[1].trim() : normP1Full.trim();
                    const normP1Stripped = valP1.replace(/\s+/g, '');
                    
                    if (!valTag || !valP1) return false;
                    
                    if (normTagStripped === normP1Stripped) return true;
                    
                    const tagWords = valTag.split(/\s+/);
                    const p1Words = valP1.split(/\s+/);
                    
                    if (valTag.length >= 3 && p1Words.includes(valTag)) return true;
                    if (valP1.length >= 3 && tagWords.includes(valP1)) return true;
                    
                    return false;
                });
                
                if (match) {
                    const isIgnoredCity = ignoreCities.some(c => c.replace(/\s+/g, '') === normTagStripped || (normTagStripped.length > 3 && normTagStripped.includes(c.replace(/\s+/g, ''))));
                    
                    // Check if tag is broad (university, degree, or generic role) to prevent double counting or over-rewarding broad tags
                    const isBroadUni = synonymGroups.some(g => g.type === 'uni' && g.words.some(w => w.replace(/\s+/g, '') === normTagStripped || cleanTag.toLowerCase().includes(w)));
                    const isBroadDegree = synonymGroups.some(g => g.type === 'degree' && g.words.some(w => w.replace(/\s+/g, '') === normTagStripped || cleanTag.toLowerCase().includes(w)));
                    const isGenericRole = genericRoles.includes(normTagStripped) || genericRoles.includes(cleanTag.toLowerCase());
                    const isHighSchool = cleanTag.toLowerCase().includes('highschool:') || valTag.toLowerCase().includes('school') || valTag.toLowerCase().includes('בית ספר') || normTagStripped.includes('hakfarhayarok') || normTagStripped.includes('kadoorie') || normTagStripped.includes('כדורי');

                    if (isIgnoredCity) {
                        // Completely ignore large cities even if similar age
                    } else if (isBroadUni) {
                        score += 2; // Negligible points for matching uni in tags
                    } else if (isBroadDegree || isGenericRole) {
                        score += 2; // Negligible points for matching generic profession in tags
                    } else if (isHighSchool && !isSimilarAge) {
                        score += 3; // Age gap > 4, so it's a weak connection
                    } else {
                        score += 15;
                        sharedStrings.push(cleanTag);
                    }
                }
            });

            // Cross-match: if p1 has a tag that matches p2's city
            p1Tags.forEach(t => {
                const cleanP1 = t.replace(/^#/, '');
                const normP1Full = cleanP1.toLowerCase();
                const valP1 = normP1Full.includes(':') ? normP1Full.split(':')[1].trim() : normP1Full.trim();
                const normP1Stripped = valP1.replace(/\s+/g, '');
                const normCity2 = p2CityLower.replace(/\s+/g, '');
                
                // Only match if exact or full word
                let crossMatch = false;
                if (normP1Stripped.length > 3 && normCity2 === normP1Stripped) crossMatch = true;
                else {
                    const cityWords = p2CityLower.split(/\||\/|,|\s-\s|—|\n|\sand\s|\s&\s|\s+/i).map(s => s.trim()).filter(Boolean);
                    if (valP1.length > 3 && cityWords.includes(valP1)) crossMatch = true;
                }
                
                if (crossMatch) {
                    const isIgnored = ignoreCities.some(c => c.replace(/\s+/g, '') === normP1Stripped || normCity2.includes(c.replace(/\s+/g, '')));
                    if (!isIgnored || isSimilarAge) {
                        score += 15;
                        sharedStrings.push(cleanP1);
                    }
                }
            });

            // Check for last name match
            if (p1.name && p2.name) {
                const ignoreLastNames = ['cohen', 'dahan', 'levi', 'levy', 'israeli', 'mizrachi', 'peretz', 'biton', 'azoulay', 'katz', 'friedman', 'shapiro', 'goldberg', 'avidan'];
                const p1Parts = p1.name.trim().split(/\s+/);
                const p2Parts = p2.name.trim().split(/\s+/);
                
                if (p1Parts.length > 1 && p2Parts.length > 1) {
                    const p1LastName = p1Parts[p1Parts.length - 1].toLowerCase();
                    const p2LastName = p2Parts[p2Parts.length - 1].toLowerCase();
                    
                    const isMishliAlias = (p1LastName === 'mishli' && p2LastName === 'mishali') || (p1LastName === 'mishali' && p2LastName === 'mishli');
                    
                    if ((p1LastName === p2LastName || isMishliAlias) && p1LastName.length > 2 && p2LastName.length > 2 && !ignoreLastNames.includes(p1LastName) && !ignoreLastNames.includes(p2LastName)) {
                        const p1OriginLower = (p1.originCity || '').toLowerCase().replace(/#/g, '');
                        let originMatch = false;
                        if (p1OriginLower && p1OriginLower.length > 2) {
                            let originWords1 = p1OriginLower.split(/\||\/|,|\s-\s|—|\n|\sand\s|\s&\s/i).map(s => s.trim()).filter(Boolean);
                            const originAliases = {
                                'ilaniya': ['ilaniya', 'ilania', 'אילניה'],
                                'ilania': ['ilaniya', 'ilania', 'אילניה'],
                                'אילניה': ['ilaniya', 'ilania', 'אילניה'],
                                'zikhron yaakov': ['zikhron yaakov', 'זכרון יעקב'],
                                'זכרון יעקב': ['zikhron yaakov', 'זכרון יעקב'],
                                'kiryat yam': ['kiryat yam', 'קרית ים', 'קריית ים'],
                                'קרית ים': ['kiryat yam', 'קרית ים', 'קריית ים'],
                                'קריית ים': ['kiryat yam', 'קרית ים', 'קריית ים'],
                                'kiryat haim': ['kiryat haim', 'קרית חיים', 'קריית חיים'],
                                'קרית חיים': ['kiryat haim', 'קרית חיים', 'קריית חיים'],
                                'קריית חיים': ['kiryat haim', 'קרית חיים', 'קריית חיים']
                            };
                            let expandedWords = [];
                            originWords1.forEach(w => {
                                expandedWords.push(w);
                                if (originAliases[w]) expandedWords.push(...originAliases[w]);
                            });
                            originMatch = expandedWords.some(w => p2Text.includes(' ' + w + ' '));
                        }
                        if (originMatch) {
                            score += 50; // Big boost to ensure suggestion
                            sharedStrings.push(`Family name: ${p1Parts[p1Parts.length - 1]}`);
                        }
                    }
                }
            }
            
            const finalShared = [...new Set(sharedStrings)];
            // If they reached score 25 but have NO explicit shared concepts, cap their score at 10
            if (finalShared.length === 0 && score >= 25) {
                score = 10;
            }
            
            return { 
                score, 
                sharedConcepts: finalShared.filter(s => !/[\u0590-\u05FF]/.test(s))
            };
        }
