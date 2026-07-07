const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf8');
const scriptMatches = [...html.matchAll(/<script.*?>([\s\S]*?)<\/script>/gi)];
scriptMatches.forEach((match, idx) => {
    const code = match[1];
    fs.writeFileSync(`temp_${idx}.js`, code);
    const { execSync } = require('child_process');
    try {
        execSync(`node --check temp_${idx}.js`, {stdio: 'pipe'});
    } catch(e) {
        console.log(`Script ${idx} Error:\n`, e.stderr.toString());
        // Calculate original line number roughly
        const preceding = html.substring(0, match.index);
        const startLine = preceding.split('\n').length;
        console.log(`Original line starts around ${startLine}`);
    }
});
