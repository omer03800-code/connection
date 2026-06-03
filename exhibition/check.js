const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf8');
const scriptMatch = html.match(/<script type="module">([\s\S]*?)<\/script>/);
if (scriptMatch) {
    fs.writeFileSync('temp_script.js', scriptMatch[1]);
    console.log('Extracted script to temp_script.js');
}
