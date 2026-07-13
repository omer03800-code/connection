const { DatabaseSync } = require('node:sqlite');
const fs = require('fs');

const data = JSON.parse(fs.readFileSync('neon_backup.json', 'utf8'));

// Delete existing to start fresh
if (fs.existsSync('db/local_backup.sqlite')) {
    fs.unlinkSync('db/local_backup.sqlite');
}

const db = new DatabaseSync('db/local_backup.sqlite');

db.exec(`
    CREATE TABLE IF NOT EXISTS people (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT NOT NULL,
        age         TEXT,
        city        TEXT,
        country     TEXT,
        role        TEXT,
        description TEXT,
        tags        TEXT,
        added_by    TEXT DEFAULT 'omer',
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS connections (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
        person_b_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
        type        TEXT NOT NULL CHECK(type IN ('family_core','family_extended','friend','acquaintance')),
        strength    INTEGER DEFAULT 3,
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(person_a_id, person_b_id)
    );

    CREATE INDEX IF NOT EXISTS idx_conn_a    ON connections(person_a_id);
    CREATE INDEX IF NOT EXISTS idx_conn_b    ON connections(person_b_id);
    CREATE INDEX IF NOT EXISTS idx_people_nm ON people(name);
`);

const insertPerson = db.prepare(`
    INSERT INTO people (id, name, age, city, country, role, description, tags, added_by, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`);

const insertConnection = db.prepare(`
    INSERT INTO connections (id, person_a_id, person_b_id, type, strength, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
`);

db.exec('BEGIN TRANSACTION');
for (const p of data.people) {
    insertPerson.run(p.id, p.name, p.age, p.city, p.country, p.role, p.description, p.tags, p.added_by, p.created_at);
}
for (const c of data.connections) {
    insertConnection.run(c.id, c.person_a_id, c.person_b_id, c.type, c.strength, c.created_at);
}
db.exec('COMMIT');

console.log("Local SQLite DB created successfully.");
