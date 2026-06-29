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
    const finalShared = [...new Set(sharedStrings)];
    return { score, sharedConcepts: finalShared };
}

const people = [
    { id: 57, city: 'Moshav Ilaniya', age: '57' },
    { id: 25, city: 'Tel Aviv', age: '30' }
];

function generateRecommendations(p1) {
    let scores = [];
    people.forEach(p => {
        const result = calculateMatchScore(p1, p);
        if (result.score >= 15 && result.sharedConcepts.length > 0) {
            scores.push({ person: p, score: result.score, shared: result.sharedConcepts });
        }
    });
    return scores.length > 0;
}

console.log("Has Recs?", generateRecommendations({ city: 'אילניה', age: '25' }));
