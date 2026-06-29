const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf8');

const regex = /function calculateMatchScore[\s\S]*?return \{[\s\S]*?score: score,[\s\S]*?sharedConcepts: Array\.from\(new Set\(sharedStrings\)\)\s*\};\s*\}/;
const match = html.match(regex);
eval(match[0]);

const p1 = { city: "ilania" };
const p2 = { city: "Moshav Ilaniya", tags: "" };

console.log(calculateMatchScore(p1, p2));
