const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf-8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
fs.writeFileSync('temp_script.js', scriptMatch[1]);
