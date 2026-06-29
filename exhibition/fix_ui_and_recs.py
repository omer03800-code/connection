import re

with open('public/index.html', 'r') as f:
    content = f.read()

# 1. Fix Popup style by adding explicit CSS
css_to_add = """
        #feed-more-popup-v2 {
            position: absolute; left: 80px; top: -10px; width: max-content; 
            padding: 20px 25px; 
            background: rgba(255, 255, 255, 0.95) !important; 
            backdrop-filter: blur(15px) !important; 
            -webkit-backdrop-filter: blur(15px) !important; 
            border-radius: 12px; pointer-events: auto; text-align: center; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.6); z-index: 100; 
            color: #0a0a0a !important;
        }
        body.light-mode #feed-more-popup-v2 {
            background: rgba(0, 0, 0, 0.95) !important; 
            color: #f5f5f5 !important;
        }
"""
if "body.light-mode #feed-more-popup-v2" not in content:
    content = content.replace('</style>', css_to_add + '\n    </style>')

# Also remove the inline style text from renderFeedMorePopup so CSS applies correctly
content = re.sub(r'feedMorePopup\.style\.cssText = "[^"]+";', '', content)

# 2. Fix the city alias matching in calculateMatchScore
match_logic_old = """            const p1CityLower = p1.city ? String(p1.city).toLowerCase() : '';
            const p2CityLower = p2.city ? String(p2.city).toLowerCase() : '';
            if (p1CityLower && p2CityLower) {
                if (p1CityLower.includes(p2CityLower) || p2CityLower.includes(p1CityLower)) {
                    score += 15;
                    finalShared.push(p1.city); // Track location match!
                }
            }"""

match_logic_new = """            const p1CityLower = p1.city ? String(p1.city).toLowerCase() : '';
            const p2CityLower = p2.city ? String(p2.city).toLowerCase() : '';
            
            // Hebrew aliases mapping
            const cityAliases = {
                'אילניה': ['ilaniya', 'ilania', 'אילניה'],
                'איניה': ['ilaniya', 'ilania', 'אילניה', 'איניה'],
                'moshav ilaniya': ['אילניה', 'ilania', 'ilaniya', 'moshav ilania', 'moshav ilaniya', 'מושב אילניה'],
                'מושב אילניה': ['ilaniya', 'ilania', 'moshav ilania', 'moshav ilaniya', 'אילניה'],
                'haifa': ['חיפה', 'haifa'],
                'חיפה': ['haifa', 'חיפה'],
                'tel aviv': ['תל אביב', 'tel aviv', 'tel-aviv'],
                'תל אביב': ['tel aviv', 'tel-aviv', 'תל אביב'],
                'ramat gan': ['רמת גן', 'ramat gan'],
                'רמת גן': ['ramat gan', 'רמת גן']
            };

            if (p1CityLower && p2CityLower) {
                let p1Vals = [p1CityLower];
                let p2Vals = [p2CityLower];
                
                Object.keys(cityAliases).forEach(k => {
                    if (p1CityLower.includes(k)) p1Vals = p1Vals.concat(cityAliases[k]);
                    if (p2CityLower.includes(k)) p2Vals = p2Vals.concat(cityAliases[k]);
                });

                const matchFound = p1Vals.some(v1 => p2Vals.some(v2 => v1.includes(v2) || v2.includes(v1)));
                if (matchFound) {
                    score += 15;
                    finalShared.push(p1.city); // Track location match!
                }
            }"""

if match_logic_old in content:
    content = content.replace(match_logic_old, match_logic_new)

# Write back
with open('public/index.html', 'w') as f:
    f.write(content)

