const Database = require('better-sqlite3');
const db = new Database('database.sqlite');
const rows = db.prepare('SELECT name, city, role, tags, description FROM people WHERE name LIKE "%Amir%"').all();
console.log(rows);
