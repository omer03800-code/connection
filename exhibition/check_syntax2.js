const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf8');
const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
if (scriptMatch) {
    try {
        new Function(scriptMatch[1]);
        console.log("Syntax is OK");
    } catch (e) {
        console.error("Syntax error:", e);
    }
}
