const ignoreCities = ['tel aviv', 'jerusalem', 'haifa', 'תל אביב', 'ירושלים', 'חיפה'];

function calculateMatchScore(p1, p2) {
    let score = 0;
    let sharedStrings = [];
    const p1CityLower = p1.city ? p1.city.toLowerCase() : '';
    const p2CityLower = p2.city ? p2.city.toLowerCase() : '';
    
    if (p1CityLower && p2CityLower) {
        const cityAliases = {
            'אילניה': ['ilaniya', 'ilania', 'אילניה'],
            'moshav ilaniya': ['אילניה', 'ilania', 'ilaniya', 'moshav ilania', 'moshav ilaniya', 'מושב אילניה'],
            'מושב אילניה': ['ilaniya', 'ilania', 'moshav ilania', 'moshav ilaniya', 'אילניה']
        };

        let p1Vals = [p1CityLower];
        let p2Vals = [p2CityLower];
        
        Object.keys(cityAliases).forEach(k => {
            if (p1CityLower.includes(k)) p1Vals = p1Vals.concat(cityAliases[k]);
            if (p2CityLower.includes(k)) p2Vals = p2Vals.concat(cityAliases[k]);
        });

        const matchFound = p1Vals.some(v1 => p2Vals.some(v2 => v1.includes(v2) || v2.includes(v1)));
        const shouldIgnore = ignoreCities.some(c => p1CityLower.includes(c)) || ignoreCities.some(c => p2CityLower.includes(c));
        
        if (matchFound) {
            if (!shouldIgnore) {
                score += 15;
                sharedStrings.push(p1CityLower);
            }
        }
    }
    return score;
}

console.log("Test:", calculateMatchScore({city: 'מושב אילניה'}, {city: 'Moshav Ilaniya'}));

