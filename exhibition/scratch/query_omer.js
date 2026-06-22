const { DatabaseSync } = require('node:sqlite');
const path = require('path');
const db = new DatabaseSync(path.join(__dirname, '../db/six-degrees.sqlite'));

const omer = db.prepare(`SELECT id, name, city, role, tags, description FROM people WHERE name LIKE '%omer barak%' OR name LIKE '%עומר ברק%'`).get();
console.log(omer);
