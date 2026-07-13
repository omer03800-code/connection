const { Router } = require('express');
const { query, db } = require('../db/schema');

const router = Router();

// GET /api/people/search/query?q=term
router.get('/search/query', async (req, res) => {
    const term = (req.query.q || '').toLowerCase();
    
    // Fetch all and filter in JS to allow proper word-boundary regex (so "ono" doesn't match "Economics")
    const allPeople = (await query(`SELECT id, name, city, role, tags, description FROM people`)).rows;
    
    let searchTerms = [term];
    
    // Search Aliases (Hebrew to English / Typos)
    const aliases = {
        'אילניה': ['ilaniya', 'ilania', 'אילניה'],
        'איניה': ['ilaniya', 'ilania', 'אילניה', 'איניה'],
        'ilaniya': ['ilaniya', 'ilania', 'אילניה'],
        'ilania': ['ilaniya', 'ilania', 'אילניה'],
        'זכרון יעקב': ['zikhron yaakov', 'זכרון יעקב', 'zikhron ya\'akov'],
        'זכרון יעקוב': ['zikhron yaakov', 'זכרון יעקב', 'zikhron ya\'akov', 'זכרון יעקוב'],
        'קרית ים': ['kiryat yam', 'קרית ים', 'קריית ים'],
        'קריית ים': ['kiryat yam', 'קרית ים', 'קריית ים'],
        'קרית חיים': ['kiryat haim', 'קרית חיים', 'קריית חיים'],
        'קריית חיים': ['kiryat haim', 'קרית חיים', 'קריית חיים'],
        'איילת השחר': ['ayelet hashahar', 'איילת השחר', 'ayelet ha-shahar', 'ayelet hashachar'],
        'גבעת אלה': ['givat ella', 'givat ela', 'גבעת אלה']
    };
    
    if (aliases[term]) {
        searchTerms = aliases[term];
    }

    // Use start of string or space/punctuation (including # for tags) to allow prefix matching
    const escapeRegExp = (string) => string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const escapedTerms = searchTerms.map(escapeRegExp).join('|');
    const regex = new RegExp(`(^|[\\s,.\\-/'"#+&()])[\\s]*(?:${escapedTerms})`, 'i');
    
    const filtered = allPeople.filter(p => {
        return regex.test(p.name) || 
               regex.test(p.city) || 
               regex.test(p.role) || 
               regex.test(p.tags) || 
               regex.test(p.description);
    }).slice(0, 30);
    
    // Clean up description before sending to save bandwidth, since UI only needs tags/roles
    const cleanFiltered = filtered.map(p => {
        const { description, ...rest } = p;
        return rest;
    });

    // Extract metadata suggestions
    const metadataSet = new Map();
    const addMeta = (type, val) => {
        if (!val) return;
        const v = val.trim();
        if (!v) return;
        const key = type + ':' + v.toLowerCase();
        if (!metadataSet.has(key)) {
            metadataSet.set(key, { type, value: v });
        }
    };

    allPeople.forEach(p => {
        if (p.city) {
            const cities = p.city.replace(/#/g, '').split(/[,/]+/).map(c => c.trim()).filter(Boolean);
            cities.forEach(c => {
                if (regex.test(c)) addMeta('LOCATION', c);
            });
        }
        if (p.role) {
            const roles = p.role.replace(/#/g, '').split(/[,/]+/).map(r => r.trim()).filter(Boolean);
            roles.forEach(r => {
                if (regex.test(r)) addMeta('ROLE', r);
            });
        }
        if (p.tags) {
            const tList = p.tags.split(/[\s,]+/);
            tList.forEach(t => {
                const cleanTag = t.replace(/^#/, '').trim();
                const isIgnored = cleanTag.toLowerCase() === 'twin' || cleanTag === 'תאומה' || cleanTag.toLowerCase() === 'telaviv';
                if (cleanTag && !isIgnored && regex.test(cleanTag)) addMeta('TAG', cleanTag);
            });
        }
    });

    const metadataMatches = Array.from(metadataSet.values()).slice(0, 5);
    
    res.json({ people: cleanFiltered, metadata: metadataMatches });
});

// GET /api/people/suggest/name?name=term
router.get('/suggest/name', async (req, res) => {
    const q = `%${(req.query.name || '').toLowerCase()}%`;
    const people = (await query(`
        SELECT id, name, city, role FROM people WHERE lower(name) LIKE ? LIMIT 5
    `, [q])).rows;
    res.json(people);
});

// GET /api/people — all people
router.get('/', async (req, res) => {
    const people = (await query(
        `SELECT id, name, age, country, city, role, tags, description FROM people ORDER BY id`
    )).rows;
    res.json(people);
});

// GET /api/people/:id
router.get('/:id', async (req, res) => {
    const person = ((await query('SELECT * FROM people WHERE id = ?', [req.params.id])).rows[0]);
    if (!person) return res.status(404).json({ error: 'Not found' });

    const connections = (await query(`
        SELECT p.id, p.name, p.role, c.type, c.strength
        FROM connections c JOIN people p ON p.id = c.person_b_id
        WHERE c.person_a_id = ?
        UNION
        SELECT p.id, p.name, p.role, c.type, c.strength
        FROM connections c JOIN people p ON p.id = c.person_a_id
        WHERE c.person_b_id = ?
        ORDER BY type, name
    `, [req.params.id, req.params.id])).rows;

    res.json({ ...person, connections });
});

const toTitleCase = (str) => {
    if (!str) return str;
    return str.replace(/\b\w/g, c => c.toUpperCase());
};

// POST /api/people
router.post('/', async (req, res) => {
    let { name, age, city, country, role, description, tags, added_by, connections: conns } = req.body;
    if (!name) return res.status(400).json({ error: 'Name is required' });

    name = toTitleCase(name);

    const existing = ((await query('SELECT id FROM people WHERE name = ?', [name])).rows[0]);
    if (existing) return res.status(409).json({ error: 'Person already exists', id: existing.id });

    const result = (await query(`
        INSERT INTO people (name, age, city, country, role, description, tags, added_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `, [name, age||null, city||null, country||null, role||null, description||null, tags||null, added_by||'visitor']));

    const newId = result.lastInsertRowid;

    if (Array.isArray(conns) && conns.length) {
        const stmt = db.prepare(
            'INSERT OR IGNORE INTO connections (person_a_id, person_b_id, type, strength) VALUES (?,?,?,?)'
        );
        db.exec('BEGIN');
        for (const c of conns) {
            if (!c.id) continue;
            const t = ['family_core','family_extended','friend','acquaintance'].includes(c.type) ? c.type : 'acquaintance';
            const s = parseInt(c.strength) || 3;
            stmt.run(newId, c.id, t, s);
            stmt.run(c.id, newId, t, s);
        }
        db.exec('COMMIT');
    }

    res.status(201).json({ id: newId, name });
});

// PUT /api/people/:id
router.put('/:id', async (req, res) => {
    const { name, age, city, country, role, description, tags, connections: conns } = req.body;

    const person = ((await query('SELECT id FROM people WHERE id = ?', [req.params.id])).rows[0]);
    if (!person) return res.status(404).json({ error: 'Person not found' });

    (await query(`
        UPDATE people SET name = ?, age = ?, city = ?, country = ?, role = ?, description = ?, tags = ?
        WHERE id = ?
    `, [name||person.name, age||null, city||null, country||null, role||null, description||null, tags||null, req.params.id]));

    db.exec('BEGIN');
    
    // First, completely delete all existing connections for this person
    (await query('DELETE FROM connections WHERE person_a_id = ? OR person_b_id = ?', [req.params.id, req.params.id]));

    // Then re-insert the updated connections
    if (Array.isArray(conns) && conns.length) {
        const stmt = db.prepare(
            'INSERT OR IGNORE INTO connections (person_a_id, person_b_id, type, strength) VALUES (?,?,?,?)'
        );
        for (const c of conns) {
            if (!c.id) continue;
            const t = ['family_core','family_extended','friend','acquaintance'].includes(c.type) ? c.type : 'acquaintance';
            const s = parseInt(c.strength) || 3;
            stmt.run(req.params.id, c.id, t, s);
            stmt.run(c.id, req.params.id, t, s);
        }
    }
    
    db.exec('COMMIT');

    res.json({ id: req.params.id, updated: true });
});

// DELETE /api/people/:id
router.delete('/:id', async (req, res) => {
    const person = ((await query('SELECT id FROM people WHERE id = ?', [req.params.id])).rows[0]);
    if (!person) return res.status(404).json({ error: 'Person not found' });

    (await query('DELETE FROM people WHERE id = ?', [req.params.id]));
    res.json({ id: req.params.id, deleted: true });
});

// POST /api/connections/direct - add a single direct connection safely
router.post('/connections/direct', async (req, res) => {
    const { person_a_id, person_b_id, type, strength } = req.body;
    
    if (!person_a_id || !person_b_id) {
        return res.status(400).json({ error: 'Missing person IDs' });
    }
    
    const t = ['family_core','family_extended','friend','acquaintance'].includes(type) ? type : 'acquaintance';
    const s = parseInt(strength) || 3;
    
    const stmt = db.prepare(
        'INSERT OR IGNORE INTO connections (person_a_id, person_b_id, type, strength) VALUES (?,?,?,?)'
    );
    
    db.exec('BEGIN');
    stmt.run(person_a_id, person_b_id, t, s);
    stmt.run(person_b_id, person_a_id, t, s);
    db.exec('COMMIT');
    
    res.status(201).json({ success: true, message: 'Connection added' });
});

module.exports = router;
