const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf-8');
const js = html.match(/<script[^>]*>([\s\S]*?)<\/script>/g).map(s => s.replace(/<script[^>]*>|<\/script>/g, '')).join('\n');
try {
    new Function(js);
    console.log("No syntax errors in inline JS.");
} catch(e) {
    console.error("Syntax error:", e);
}
