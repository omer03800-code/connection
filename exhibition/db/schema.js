const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    connectionString: process.env.DATABASE_URL || process.env.POSTGRES_URL,
});

async function initSchema() {
    try {
        await pool.query(`
            CREATE TABLE IF NOT EXISTS people (
                id          SERIAL PRIMARY KEY,
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
                id          SERIAL PRIMARY KEY,
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
        console.log("Database schema initialized successfully.");
    } catch (err) {
        console.error("Error initializing schema:", err);
    }
}

initSchema();

module.exports = {
    query: (text, params) => {
        if (params && params.length > 0) {
            let i = 1;
            text = text.replace(/\?/g, () => `$${i++}`);
        }
        return pool.query(text, params);
    },
};
