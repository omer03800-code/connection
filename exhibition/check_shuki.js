const { Pool } = require('pg');
require('dotenv').config();
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
async function main() {
    const res = await pool.query("SELECT age, country, city FROM people WHERE name = 'Shuki Weiss'");
    console.log(res.rows);
    pool.end();
}
main();
