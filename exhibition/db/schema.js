const { DatabaseSync } = require('node:sqlite');
const path = require('path');

const DB_PATH = path.join(__dirname, 'six-degrees.sqlite');

let db;
function getDb() {
    if (!db) {
        db = new DatabaseSync(DB_PATH);
        db.exec('PRAGMA journal_mode=WAL');
        db.exec('PRAGMA foreign_keys=ON');
        initSchema();
    }
    return db;
}

function initSchema() {
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
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS connections (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
            person_b_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
            type        TEXT NOT NULL CHECK(type IN ('family_core','family_extended','friend','acquaintance')),
            strength    INTEGER DEFAULT 3,
            created_at  TEXT DEFAULT (datetime('now')),
            UNIQUE(person_a_id, person_b_id)
        );

        CREATE INDEX IF NOT EXISTS idx_conn_a    ON connections(person_a_id);
        CREATE INDEX IF NOT EXISTS idx_conn_b    ON connections(person_b_id);
        CREATE INDEX IF NOT EXISTS idx_people_nm ON people(name);
    `);
}

module.exports = { getDb };
