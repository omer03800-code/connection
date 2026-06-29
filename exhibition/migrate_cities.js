const { DatabaseSync } = require('node:sqlite');
const db = new DatabaseSync('./db/six-degrees.sqlite');

const stmt = db.prepare(`SELECT id, city, description FROM people WHERE lower(description) LIKE '%originally from%'`);
const people = stmt.all();

let updated = 0;
for (const p of people) {
    const desc = p.description || '';
    
    // match "Originally from X." or "[Originally from X]" or "Originally from X"
    const regex = /Originally from\s+([^\].,\n]+)/i;
    const match = desc.match(regex);
    
    if (match) {
        let originCity = match[1].trim();
        originCity = originCity.replace(/['"]+$/, '').trim();
        
        const currentCity = (p.city || '').trim();
        
        if (currentCity.toLowerCase().indexOf(originCity.toLowerCase()) === -1) {
            const newCity = currentCity ? `${currentCity}, ${originCity}` : originCity;
            
            console.log(`Updating ID ${p.id}: City "${currentCity}" -> "${newCity}"`);
            const updateStmt = db.prepare(`UPDATE people SET city = ? WHERE id = ?`);
            updateStmt.run(newCity, p.id);
            updated++;
        }
    }
}

console.log(`Updated ${updated} people.`);
