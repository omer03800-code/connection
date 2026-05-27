const { getDb } = require('../db/schema');
const fs = require('fs');
const path = require('path');

const PEOPLE_CSV      = path.join(__dirname, '../../אקסלים data/Omer_Network_People.csv');
const CONNECTIONS_CSV = path.join(__dirname, '../../אקסלים data/just connect.csv');

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

    // Core family members (immediate family of Omer)
    const coreFamilyNames = new Set(['Omer Barak', 'Noa Barak', 'Eti Barak', 'Eli Barak']);

    // Import people
    const peopleRaw = parseCSV(fs.readFileSync(PEOPLE_CSV, 'utf8'));
    const insertPerson = db.prepare(`
        INSERT INTO people (name, age, city, country, role, description, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `);

    const nameToId = {};
    db.exec('BEGIN');
    for (const row of peopleRaw) {
        if (!row.Name) continue;
        const result = insertPerson.run(
            row.Name,
            row.Age || null,
            row.City || null,
            row.Country || null,
            row.Role || null,
            row.Description || null,
            row.Tags || null
        );
        nameToId[row.Name] = result.lastInsertRowid;
    }
    db.exec('COMMIT');
    console.log(`✓ Imported ${Object.keys(nameToId).length} people`);

    // Import connections
    const connectionsRaw = parseCSV(fs.readFileSync(CONNECTIONS_CSV, 'utf8'));
    const insertConn = db.prepare(`
        INSERT OR IGNORE INTO connections (person_a_id, person_b_id, type, strength)
        VALUES (?, ?, ?, ?)
    `);

    let connCount = 0;
    db.exec('BEGIN');
    for (const row of connectionsRaw) {
        const a = nameToId[row.Source];
        const b = nameToId[row.Target];
        if (!a || !b) {
            if (row.Source) console.warn(`  ⚠ Unknown: "${row.Source}" → "${row.Target}"`);
            continue;
        }

        // Split family into family_core and family_extended
        let type = row.Type;
        if (row.Type === 'family') {
            const bothCore = coreFamilyNames.has(row.Source) && coreFamilyNames.has(row.Target);
            type = bothCore ? 'family_core' : 'family_extended';
        }

        // Validate type
        if (!['family_core','family_extended','friend','acquaintance'].includes(type)) {
            type = 'acquaintance';
        }

        const strength = parseInt(row.Strength) || 3;
        insertConn.run(a, b, type, strength);
        insertConn.run(b, a, type, strength);
        connCount++;
    }
    db.exec('COMMIT');
    console.log(`✓ Imported ${connCount} connections`);
    console.log('Database ready:', path.join(__dirname, '../db/six-degrees.sqlite'));
}

run();
