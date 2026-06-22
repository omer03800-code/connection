const { DatabaseSync } = require('node:sqlite');
const path = require('path');
const db = new DatabaseSync(path.join(__dirname, '../db/six-degrees.sqlite'));

const term = 'ilania'.toLowerCase();
const allPeople = db.prepare(`SELECT id, name, city, role, tags, description FROM people`).all();

let searchTerms = [term];
const aliases = {
    'אילניה': ['ilaniya', 'ilania', 'אילניה'],
    'איניה': ['ilaniya', 'ilania', 'אילניה', 'איניה'],
    'ilaniya': ['ilaniya', 'ilania', 'אילניה'],
    'ilania': ['ilaniya', 'ilania', 'אילניה']
};

if (aliases[term]) {
    searchTerms = aliases[term];
}

const escapeRegExp = (string) => string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const escapedTerms = searchTerms.map(escapeRegExp).join('|');
const regex = new RegExp(`(^|[\\s,.\\-/'"#+&()])[\\s]*(?:${escapedTerms})`, 'i');

console.log("Regex:", regex.toString());

const filtered = allPeople.filter(p => {
    return regex.test(p.name) || 
           regex.test(p.city) || 
           regex.test(p.role) || 
           regex.test(p.tags) || 
           regex.test(p.description);
});

console.log("Matched", filtered.length, "people:");
console.log(filtered.map(p => p.name));
