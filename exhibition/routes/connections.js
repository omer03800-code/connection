const { Router } = require('express');
const { getDb } = require('../db/schema');

const router = Router();

// GET /api/connections/path/:from/:to — BFS shortest path
router.get('/path/:from/:to', (req, res) => {
    const db = getDb();
    const fromId = parseInt(req.params.from);
    const toId   = parseInt(req.params.to);

    if (fromId === toId) {
        const p = db.prepare('SELECT id, name FROM people WHERE id = ?').get(fromId);
        return res.json({ path: p ? [p] : [], degrees: 0 });
    }

    const rows = db.prepare('SELECT person_a_id, person_b_id FROM connections').all();
    const adj = {};
    for (const r of rows) {
        if (!adj[r.person_a_id]) adj[r.person_a_id] = [];
        adj[r.person_a_id].push(r.person_b_id);
    }

    const visited = new Set([fromId]);
    const queue = [[fromId]];
    while (queue.length) {
        const path = queue.shift();
        const node = path[path.length - 1];
        for (const neighbor of (adj[node] || [])) {
            if (!visited.has(neighbor)) {
                const newPath = [...path, neighbor];
                if (neighbor === toId) {
                    const placeholders = newPath.map(() => '?').join(',');
                    const people = db.prepare(
                        `SELECT id, name FROM people WHERE id IN (${placeholders})`
                    ).all(...newPath);
                    const byId = Object.fromEntries(people.map(p => [p.id, p]));
                    return res.json({ path: newPath.map(id => byId[id]), degrees: newPath.length - 1 });
                }
                visited.add(neighbor);
                queue.push(newPath);
            }
        }
    }
    res.json({ path: null, degrees: -1 });
});

// GET /api/connections — all connections
router.get('/', (req, res) => {
    const db = getDb();
    const conns = db.prepare(
        'SELECT person_a_id as source, person_b_id as target, type, strength FROM connections WHERE person_a_id < person_b_id'
    ).all();
    res.json(conns);
});

// POST /api/connections
router.post('/', (req, res) => {
    const db = getDb();
    const { person_a_id, person_b_id, type, strength } = req.body;
    if (!person_a_id || !person_b_id) return res.status(400).json({ error: 'person_a_id and person_b_id required' });

    const t = ['family','friend','acquaintance'].includes(type) ? type : 'acquaintance';
    const s = parseInt(strength) || 3;
    const stmt = db.prepare('INSERT OR IGNORE INTO connections (person_a_id, person_b_id, type, strength) VALUES (?,?,?,?)');
    stmt.run(person_a_id, person_b_id, t, s);
    stmt.run(person_b_id, person_a_id, t, s);
    res.status(201).json({ ok: true });
});

module.exports = router;
