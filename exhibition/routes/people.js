const { Router } = require('express');
const { getDb } = require('../db/schema');

const router = Router();

// GET /api/people/search/query?q=term
router.get('/search/query', (req, res) => {
    const db = getDb();
    const q = `%${(req.query.q || '').toLowerCase()}%`;
    const people = db.prepare(`
        SELECT id, name, city, role, tags
        FROM people
        WHERE lower(name) LIKE ? OR lower(city) LIKE ? OR lower(role) LIKE ?
           OR lower(tags) LIKE ? OR lower(coalesce(description,'')) LIKE ?
        LIMIT 30
    `).all(q, q, q, q, q);
    res.json(people);
});

// GET /api/people/suggest/name?name=term
router.get('/suggest/name', (req, res) => {
    const db = getDb();
    const q = `%${(req.query.name || '').toLowerCase()}%`;
    const people = db.prepare(`
        SELECT id, name, city, role FROM people WHERE lower(name) LIKE ? LIMIT 5
    `).all(q);
    res.json(people);
});

// GET /api/people — all people
router.get('/', (req, res) => {
    const db = getDb();
    const people = db.prepare(
        'SELECT id, name, age, city, country, role, description, tags FROM people ORDER BY id'
    ).all();
    res.json(people);
});

// GET /api/people/:id
router.get('/:id', (req, res) => {
    const db = getDb();
    const person = db.prepare('SELECT * FROM people WHERE id = ?').get(req.params.id);
    if (!person) return res.status(404).json({ error: 'Not found' });

    const connections = db.prepare(`
        SELECT p.id, p.name, p.role, c.type, c.strength
        FROM connections c JOIN people p ON p.id = c.person_b_id
        WHERE c.person_a_id = ?
        UNION
        SELECT p.id, p.name, p.role, c.type, c.strength
        FROM connections c JOIN people p ON p.id = c.person_a_id
        WHERE c.person_b_id = ?
        ORDER BY type, name
    `).all(req.params.id, req.params.id);

    res.json({ ...person, connections });
});

// POST /api/people
router.post('/', (req, res) => {
    const db = getDb();
    const { name, age, city, country, role, description, tags, added_by, connections: conns } = req.body;
    if (!name) return res.status(400).json({ error: 'name is required' });

    const existing = db.prepare('SELECT id FROM people WHERE name = ?').get(name);
    if (existing) return res.status(409).json({ error: 'Person already exists', id: existing.id });

    const result = db.prepare(`
        INSERT INTO people (name, age, city, country, role, description, tags, added_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(name, age||null, city||null, country||null, role||null, description||null, tags||null, added_by||'visitor');

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
router.put('/:id', (req, res) => {
    const db = getDb();
    const { age, city, country, role, description, tags, connections: conns } = req.body;

    const person = db.prepare('SELECT id FROM people WHERE id = ?').get(req.params.id);
    if (!person) return res.status(404).json({ error: 'Person not found' });

    db.prepare(`
        UPDATE people SET age = ?, city = ?, country = ?, role = ?, description = ?, tags = ?
        WHERE id = ?
    `).run(age||null, city||null, country||null, role||null, description||null, tags||null, req.params.id);

    if (Array.isArray(conns) && conns.length) {
        const stmt = db.prepare(
            'INSERT OR IGNORE INTO connections (person_a_id, person_b_id, type, strength) VALUES (?,?,?,?)'
        );
        db.exec('BEGIN');
        for (const c of conns) {
            if (!c.id) continue;
            const t = ['family_core','family_extended','friend','acquaintance'].includes(c.type) ? c.type : 'acquaintance';
            const s = parseInt(c.strength) || 3;
            stmt.run(req.params.id, c.id, t, s);
            stmt.run(c.id, req.params.id, t, s);
        }
        db.exec('COMMIT');
    }

    res.json({ id: req.params.id, updated: true });
});

// DELETE /api/people/:id
router.delete('/:id', (req, res) => {
    const db = getDb();
    const person = db.prepare('SELECT id FROM people WHERE id = ?').get(req.params.id);
    if (!person) return res.status(404).json({ error: 'Person not found' });

    db.prepare('DELETE FROM people WHERE id = ?').run(req.params.id);
    res.json({ id: req.params.id, deleted: true });
});

module.exports = router;
