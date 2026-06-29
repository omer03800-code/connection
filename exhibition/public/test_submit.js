const fs = require('fs');
const html = fs.readFileSync('/Users/omerbarak/Documents/פגמר/exhibition/public/index.html', 'utf8');

const regex = /document\.getElementById\(['"]([^'"]+)['"]\)/g;
let match;
const ids = new Set();
while ((match = regex.exec(html)) !== null) {
    ids.add(match[1]);
}

const missing = [];
const expected = ['f-birth-year', 'tw-f-city', 'f-city', 'tw-f-workplace', 'f-workplace', 'f-highschool', 'f-university', 'f-degree', 'f-army-role', 'f-army-base', 'tw-f-other-value', 'f-other-value', 'f-tags', 'f-desc', 'f-name', 'tw-f-role', 'f-role', 'f-country', 'tw-f-origin-city', 'f-origin-city'];

for (const id of expected) {
    if (!html.includes(`id="${id}"`) && !html.includes(`id='${id}'`)) {
        missing.push(id);
    }
}
console.log("Missing IDs:", missing);
