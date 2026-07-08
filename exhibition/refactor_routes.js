const fs = require('fs');
const path = require('path');

const routesDir = path.join(__dirname, 'routes');
const files = ['people.js', 'connections.js', 'suggest.js'];

files.forEach(file => {
    const filePath = path.join(routesDir, file);
    let content = fs.readFileSync(filePath, 'utf8');

    // Change import
    content = content.replace(/const\s+\{\s*getDb\s*\}\s*=\s*require\('\.\.\/db\/schema'\);/g, "const { query } = require('../db/schema');");

    // Change all router endpoints to async
    content = content.replace(/router\.(get|post|put|delete)\('([^']+)',\s*(async\s*)?\(req,\s*res\)\s*=>\s*\{/g, "router.$1('$2', async (req, res) => {");

    // Remove const db = getDb();
    content = content.replace(/\s*const\s+db\s*=\s*getDb\(\);\n?/g, "\n");

    // Replace db.prepare(...).all() with no args
    content = content.replace(/db\.prepare\((`[^`]+`|'[^']+'|"[^"]+")\)\.all\(\)/g, "(await query($1)).rows");

    // Replace db.prepare(...).all(args)
    content = content.replace(/db\.prepare\((`[^`]+`|'[^']+'|"[^"]+")\)\.all\(([^)]+)\)/g, "(await query($1, [$2])).rows");

    // Replace db.prepare(...).get() with no args
    content = content.replace(/db\.prepare\((`[^`]+`|'[^']+'|"[^"]+")\)\.get\(\)/g, "((await query($1)).rows[0])");

    // Replace db.prepare(...).get(args)
    content = content.replace(/db\.prepare\((`[^`]+`|'[^']+'|"[^"]+")\)\.get\(([^)]+)\)/g, "((await query($1, [$2])).rows[0])");

    // Replace db.prepare(...).run() with no args
    content = content.replace(/db\.prepare\((`[^`]+`|'[^']+'|"[^"]+")\)\.run\(\)/g, "(await query($1))");

    // Replace db.prepare(...).run(args)
    content = content.replace(/db\.prepare\((`[^`]+`|'[^']+'|"[^"]+")\)\.run\(([^)]+)\)/g, "(await query($1, [$2]))");

    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Refactored ${file}`);
});
