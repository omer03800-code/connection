const { getDb } = require('../db/schema');
const fs = require('fs');
const path = require('path');

const CSV_FILE = path.join(__dirname, '../../אקסלים data/Omer_Connections_v12.csv');

function parseCSV(text) {
    const lines = text.split('\n').filter(l => l.trim());
    const headers = parseRow(lines[0]);
    return lines.slice(1).map(line => {
        const values = parseRow(line);
        const obj = {};
        headers.forEach((h, i) => { obj[h.trim()] = (values[i] || '').trim(); });
        return obj;
    });
}

function parseRow(line) {
    const result = [];
    let current = '';
    let inQuotes = false;
    for (const ch of line) {
        if (ch === '"') { inQuotes = !inQuotes; }
        else if (ch === ',' && !inQuotes) { result.push(current); current = ''; }
        else { current += ch; }
    }
    result.push(current);
    return result;
}

function run() {
    const db = getDb();
    db.exec('DELETE FROM connections; DELETE FROM people; DELETE FROM sqlite_sequence;');

    const coreFamilyNames = new Set(['Omer Barak', 'Noa Barak', 'Eti Barak', 'Eli Barak']);
    const rawData = parseCSV(fs.readFileSync(CSV_FILE, 'utf8'));
    
    const insertPerson = db.prepare(`
        INSERT INTO people (name, age, city, country, role, description, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `);
    
    const insertConn = db.prepare(`
        INSERT OR IGNORE INTO connections (person_a_id, person_b_id, type, strength)
        VALUES (?, ?, ?, ?)
    `);

    const nameToId = {};
    
    // First pass: Insert all source people with their full data
    db.exec('BEGIN');
    for (const row of rawData) {
        const name = row.name;
        if (!name || nameToId[name]) continue;
        
        const result = insertPerson.run(
            name,
            row.age || null,
            row.city || null,
            row.country || null,
            row.role || null,
            row.description || null,
            row.tags || null
        );
        nameToId[name] = result.lastInsertRowid;
    }
    
    // Second pass: Insert target people if they don't exist, then insert connections
    let connCount = 0;
    for (const row of rawData) {
        const sourceName = row.name;
        const targetName = row.connected_to;
        
        if (!sourceName || !targetName || targetName === 'N/A') continue;
        
        // Auto-create target if missing
        if (!nameToId[targetName]) {
            const result = insertPerson.run(targetName, null, null, null, 'Known Connection', null, null);
            nameToId[targetName] = result.lastInsertRowid;
        }
        
        const a = nameToId[sourceName];
        const b = nameToId[targetName];
        
        let type = row.type || 'acquaintance';
        if (type === 'family') {
            const bothCore = coreFamilyNames.has(sourceName) && coreFamilyNames.has(targetName);
            type = bothCore ? 'family_core' : 'family_extended';
        }
        if (!['family_core','family_extended','friend','acquaintance'].includes(type)) {
            type = 'acquaintance';
        }
        
        const strength = parseInt(row.strength) || 3;
        insertConn.run(a, b, type, strength);
        insertConn.run(b, a, type, strength);
        connCount++;
    }
    
    db.exec('COMMIT');
    console.log(`✓ Imported ${Object.keys(nameToId).length} people`);
    console.log(`✓ Imported ${connCount} connections`);
    console.log('Database ready:', path.join(__dirname, '../db/six-degrees.sqlite'));
}

run();
