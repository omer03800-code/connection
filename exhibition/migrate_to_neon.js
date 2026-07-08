require('dotenv').config();
const { DatabaseSync } = require('node:sqlite');
const { Pool } = require('pg');
const path = require('path');
require('./db/schema');

const DB_PATH = path.join(__dirname, 'db', 'six-degrees.sqlite');
const sqliteDb = new DatabaseSync(DB_PATH);

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
});

async function migrate() {
    try {
        console.log("Connecting to Postgres...");
        await pool.query('SELECT 1'); // test connection

        console.log("Reading local data...");
        const people = sqliteDb.prepare('SELECT * FROM people').all();
        const rawConnections = sqliteDb.prepare('SELECT * FROM connections').all();
        const peopleMap = new Set(people.map(p => p.id));
        const connections = rawConnections.filter(c => peopleMap.has(c.person_a_id) && peopleMap.has(c.person_b_id));
        console.log(`Found ${people.length} people and ${connections.length} valid connections locally (discarded ${rawConnections.length - connections.length} orphaned).`);

        // Clear existing postgres data
        console.log("Clearing Postgres database...");
        await pool.query('TRUNCATE TABLE connections, people RESTART IDENTITY CASCADE');

        console.log("Inserting people...");
        for (const p of people) {
            await pool.query(
                `INSERT INTO people (id, name, age, city, country, role, description, tags, added_by, created_at) 
                 VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
                [p.id, p.name, p.age, p.city, p.country, p.role, p.description, p.tags, p.added_by, p.created_at]
            );
        }
        
        // Sync the sequence since we inserted specific IDs
        await pool.query(`SELECT setval('people_id_seq', (SELECT MAX(id) FROM people))`);

        console.log("Inserting connections...");
        for (const c of connections) {
            await pool.query(
                `INSERT INTO connections (id, person_a_id, person_b_id, type, strength, created_at) 
                 VALUES ($1, $2, $3, $4, $5, $6)`,
                [c.id, c.person_a_id, c.person_b_id, c.type, c.strength, c.created_at]
            );
        }
        
        await pool.query(`SELECT setval('connections_id_seq', (SELECT MAX(id) FROM connections))`);

        console.log("Migration complete!");
    } catch (e) {
        console.error("Migration failed:", e);
    } finally {
        await pool.end();
    }
}

migrate();
