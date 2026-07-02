const { getDb } = require('./db/schema');
const db = getDb();

const updates = [
  { name: "Maya Bronshtein", age: "38" },
  { name: "Amos Adler", age: "39" },
  { name: "Ariel Bronshtein", age: "36" },
  { name: "Lior Ashel", age: "42" },
  { name: "Ben Ashel", age: "38" },
  { name: "Nira Hamelach", age: "70" },
  { name: "Moti Melach", age: "71" },
  { name: "Shani Golov", age: "4" },
  { name: "Dani Levi", age: "30" },
  { name: "Yoel Zajdner", age: "26" },
  { name: "Kim Kardashian", age: "45" },
  { name: "Elon Musk", age: "55" },
  { name: "Liat Malach", age: "45" },
  { name: "Assaf Golov", age: "47" },
  { name: "Lital Ashel", age: "38" },
  { name: "Dana Rik Ashel", age: "38" }
];

const updateStmt = db.prepare("UPDATE people SET age = ? WHERE name = ?");
for (const u of updates) {
  updateStmt.run(u.age, u.name);
  console.log(`Updated ${u.name}`);
}

const noam = db.prepare("SELECT id FROM people WHERE name = 'Noam'").get();
if (noam) {
  db.prepare("DELETE FROM connections WHERE person_a_id = ? OR person_b_id = ?").run(noam.id, noam.id);
  db.prepare("DELETE FROM people WHERE id = ?").run(noam.id);
  console.log("Deleted Noam and his connections.");
}

console.log("Done!");
