const { Pool } = require('pg');
const fs = require('fs');
require('dotenv').config();
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
let funcStr = fs.readFileSync('calc.js', 'utf8');
global.window = {};
eval("window.calculateMatchScore = " + funcStr.trim());

async function main() {
    const res = await pool.query('SELECT * FROM people');
    const people = res.rows;
    const connRes = await pool.query('SELECT * FROM connections');
    const connSet = new Set(connRes.rows.map(c => c.person1_id + '-' + c.person2_id).concat(connRes.rows.map(c => c.person2_id + '-' + c.person1_id)));
    let suggestions = {};
    for (let i = 0; i < people.length; i++) {
        for (let j = i+1; j < people.length; j++) {
            if (connSet.has(people[i].id + '-' + people[j].id)) continue;
            let scoreData = window.calculateMatchScore(people[i], people[j]);
            if (scoreData.score >= 35) {
                if (!suggestions[people[i].name]) suggestions[people[i].name] = [];
                suggestions[people[i].name].push(people[j].name + " (" + scoreData.score + ")");
                if (!suggestions[people[j].name]) suggestions[people[j].name] = [];
                suggestions[people[j].name].push(people[i].name + " (" + scoreData.score + ")");
            }
        }
    }
    for (const [name, recs] of Object.entries(suggestions)) {
        console.log("- " + name + ": " + recs.slice(0, 3).join(", "));
    }
    pool.end();
}
main();
