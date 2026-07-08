const http = require('http');
const fs = require('fs');

const fetchJSON = (url) => new Promise((resolve, reject) => {
    http.get(url, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
});

async function run() {
    const people = await fetchJSON('http://127.0.0.1:1337/api/people');
    const connections = await fetchJSON('http://127.0.0.1:1337/api/connections');

    people.forEach(p => p.connections = []);
    connections.forEach(c => {
        const p1 = people.find(p => p.id === c.source);
        const p2 = people.find(p => p.id === c.target);
        if (p1) p1.connections.push({ id: c.target, type: c.type, strength: c.strength });
        if (p2) p2.connections.push({ id: c.source, type: c.type, strength: c.strength });
    });

    const matchLogic = fs.readFileSync('./scratch_match.js', 'utf8');
    eval(matchLogic);

    let peopleWithSuggestions = [];

    people.forEach(person => {
        let suggestions = [];
        people.forEach(p => {
            if (p.id === person.id) return;
            if (person.connections.some(c => c.id === p.id)) return;
            
            const result = calculateMatchScore(person, p);
            if (result.score >= 25) { // << THIS IS THE REAL THRESHOLD IN INDEX.HTML
                suggestions.push({ person: p, score: result.score, reasons: result.sharedConcepts });
            }
        });
        if (suggestions.length > 0) {
            peopleWithSuggestions.push({ name: person.name, count: suggestions.length });
        }
    });
    
    peopleWithSuggestions.sort((a,b) => b.count - a.count);
    
    console.log("Threshold >= 25:");
    console.log(peopleWithSuggestions.slice(0, 10).map(p => `${p.name} (${p.count} suggestions)`).join('\n'));
}
run();
