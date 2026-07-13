const { Pool } = require('pg');
const fs = require('fs');
require('dotenv').config();

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function exportData() {
    console.log("Exporting from Neon...");
    const people = await pool.query('SELECT * FROM people');
    const connections = await pool.query('SELECT * FROM connections');
    
    fs.writeFileSync('neon_backup.json', JSON.stringify({
        people: people.rows,
        connections: connections.rows
    }, null, 2));
    
    console.log(`Saved ${people.rows.length} people and ${connections.rows.length} connections to neon_backup.json`);
    pool.end();
}

exportData();
