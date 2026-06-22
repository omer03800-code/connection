const { DatabaseSync } = require('node:sqlite');
const path = require('path');
const db = new DatabaseSync(path.join(__dirname, '../db/six-degrees.sqlite'));

const omer = db.prepare("SELECT * FROM people WHERE name LIKE '%Omer Barak%'").get();
console.log(JSON.stringify(omer, null, 2));

const ilaniya = db.prepare("SELECT * FROM people WHERE city LIKE '%ilaniya%' OR tags LIKE '%ilaniya%' OR description LIKE '%ilaniya%' OR city LIKE '%אילניה%' OR tags LIKE '%אילניה%' OR description LIKE '%אילניה%'").all();
console.log("People in Ilaniya:", JSON.stringify(ilaniya, null, 2));
