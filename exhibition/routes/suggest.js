const { Router } = require('express');
const { query } = require('../db/schema');
const { suggestConnections } = require('../lib/smart-match');

const router = Router();

// POST /api/suggest
// Body: { name, age, city, role, description, tags, existingConnectionIds: [] }
// Returns: [{ person, score, reasons }]
router.post('/', async (req, res) => {
    const { name, age, city, role, description, tags, existingConnectionIds = [] } = req.body;

    const allPeople = (await query(
        'SELECT id, name, age, city, role, description, tags FROM people ORDER BY id'
    )).rows;

    // Build adjacency map for mutual-friend scoring
    const connRows = (await query('SELECT person_a_id, person_b_id FROM connections')).rows;
    const adjacencyMap = {};
    for (const r of connRows) {
        if (!adjacencyMap[r.person_a_id]) adjacencyMap[r.person_a_id] = [];
        adjacencyMap[r.person_a_id].push(r.person_b_id);
    }

    const candidate = { name, age, city, role, description, tags };
    const suggestions = suggestConnections(candidate, allPeople, existingConnectionIds, adjacencyMap);

    res.json(suggestions);
});

// GET /api/suggest/:id — suggest connections for an existing person in the DB
router.get('/:id', async (req, res) => {
    const person = ((await query('SELECT * FROM people WHERE id = ?', [req.params.id])).rows[0]);
    if (!person) return res.status(404).json({ error: 'Not found' });

    const allPeople = (await query(
        'SELECT id, name, age, city, role, description, tags FROM people ORDER BY id'
    )).rows;

    const connRows = (await query('SELECT person_a_id, person_b_id FROM connections')).rows;
    const adjacencyMap = {};
    for (const r of connRows) {
        if (!adjacencyMap[r.person_a_id]) adjacencyMap[r.person_a_id] = [];
        adjacencyMap[r.person_a_id].push(r.person_b_id);
    }

    const existingIds = (adjacencyMap[person.id] || []);
    const suggestions = suggestConnections(person, allPeople, existingIds, adjacencyMap);

    res.json(suggestions);
});

module.exports = router;
