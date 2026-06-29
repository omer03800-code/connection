function calculateMatchScore(p1, p2) {
    const p1CityLower = p1.city ? p1.city.toLowerCase() : '';
    const p2CityLower = p2.city ? p2.city.toLowerCase() : '';
    let score = 0;
    let sharedStrings = [];

    if (p1CityLower && p2CityLower) {
        let p1Vals = p1CityLower.split(/\||\/|,|\s-\s|—|\n|\sand\s|\s&\s/i).map(s => s.trim()).filter(Boolean);
        let p2Vals = p2CityLower.split(/\||\/|,|\s-\s|—|\n|\sand\s|\s&\s/i).map(s => s.trim()).filter(Boolean);
        
        let expandedP1Vals = [...p1Vals];
        let expandedP2Vals = [...p2Vals];

        let matchFound = false;
        let matchedVal = '';
        expandedP1Vals.forEach(v1 => {
            expandedP2Vals.forEach(v2 => {
                if (v1.includes(v2) || v2.includes(v1)) {
                    matchFound = true;
                    matchedVal = v1.length < v2.length ? v1 : v2;
                }
            });
        });
        
        if (matchFound) {
            score += 15;
            sharedStrings.push(matchedVal);
        }
    }
    return {score, sharedConcepts: sharedStrings, p1Vals: p1CityLower.split(/\||\/|,|\s-\s|—|\n|\sand\s|\s&\s/i)};
}

const p1 = {city: "kfar sirkin and kfar yona"};
const p2 = {city: "Ramat Gan and Kfar Sirkin"};
console.log(calculateMatchScore(p1, p2));
