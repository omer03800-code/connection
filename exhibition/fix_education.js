const Database = require('better-sqlite3');
const db = new Database('db/six-degrees.sqlite');

const names = [
    "Omer Barak",
    "Mai Mishli",
    "Shani Libner",
    "Shaked Klett",
    "Shaked Hogi",
    "Yoel Zajdner",
    "Shachar Liz Ben Or",
    "Ravid Dar",
    "Noya Ma'or",
    "Hila Lustig",
    "Sharon Greenberg",
    "Almog Aspaler",
    "Hila Ben Shabbat",
    "Oral Shafsha",
    "Re'ut Birkenstein"
];

for (const name of names) {
    const person = db.prepare('SELECT id, description, tags FROM people WHERE name = ?').get(name);
    if (!person) {
        console.log(`Not found: ${name}`);
        continue;
    }

    let tags = person.tags || '';
    let desc = person.description || '';

    // Remove existing university, degree, graduation year from tags
    let tagsList = tags.split(',').map(t => t.trim()).filter(Boolean);
    tagsList = tagsList.filter(t => {
        const lower = t.toLowerCase();
        return !lower.startsWith('university:') && 
               !lower.startsWith('degree:') && 
               !lower.startsWith('graduation year:');
    });

    // Add new ones
    tagsList.push('university:University of Haifa');
    tagsList.push('degree:Visual Communication');
    tagsList.push('Graduation Year:2026');

    tags = tagsList.join(', ');

    // Remove existing from desc
    let descLines = desc.split('\n').map(l => l.trim());
    descLines = descLines.filter(l => {
        const lower = l.toLowerCase();
        return !lower.startsWith('university:') && 
               !lower.startsWith('degree:') && 
               !lower.startsWith('graduation year:');
    });

    // Add new ones
    descLines.push('university: University of Haifa');
    descLines.push('degree: Visual Communication');
    descLines.push('Graduation Year: 2026');

    desc = descLines.join('\n');

    db.prepare('UPDATE people SET tags = ?, description = ? WHERE id = ?').run(tags, desc, person.id);
    console.log(`Updated: ${name}`);
}
console.log('Done.');
