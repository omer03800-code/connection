const { Pool } = require('pg');
require('dotenv').config();
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
async function main() {
    const res = await pool.query('SELECT * FROM people WHERE name = $1', ['Shuki Weiss']);
    console.log(res.rows[0]);
    pool.end();
}
main();
