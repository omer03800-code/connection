const sqlite3 = require('sqlite3');
const db = new sqlite3.Database('/Users/omerbarak/Documents/פגמר/exhibition/db/six-degrees.sqlite');

db.all("SELECT id, name FROM people WHERE name LIKE '%Tamari%' OR name LIKE '%Yarden%';", [], (err, rows) => {
    if (err) console.error(err);
    console.log(rows);
});
