require('dotenv').config();
const express = require('express');
const path = require('path');
const { query } = require('./db/schema');

const app = express();
const PORT = process.env.PORT || 1337;

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.header('Pragma', 'no-cache');
    res.header('Expires', '0');
    if (req.method === 'OPTIONS') return res.sendStatus(200);
    next();
});

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// API routes
app.use('/api/people',      require('./routes/people'));
app.use('/api/connections', require('./routes/connections'));
app.use('/api/suggest',     require('./routes/suggest'));
app.use('/api/report',      require('./routes/report'));

// GET /api/graph — full graph (all people + all connections) — convenience endpoint
app.get('/api/graph', async (req, res) => {
    try {
        const { rows: people } = await query('SELECT id, name, age, city, country, role, description, tags FROM people ORDER BY id');
        const { rows: connections } = await query(
            'SELECT person_a_id as source, person_b_id as target, type, strength FROM connections WHERE person_a_id < person_b_id'
        );
        res.json({ people, connections });
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// Health check
app.get('/api/health', async (req, res) => {
    try {
        const { rows: pRows } = await query('SELECT COUNT(*) as count FROM people');
        const { rows: cRows } = await query('SELECT COUNT(*) as count FROM connections WHERE person_a_id < person_b_id');
        res.json({ ok: true, people: pRows[0].count, connections: cRows[0].count });
    } catch (e) {
        res.status(500).json({ ok: false, error: e.message });
    }
});

// Serve the visualization for any other route
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '127.0.0.1', () => {
    console.log(`\n🌐 Feed the Beast Exhibition running at http://127.0.0.1:${PORT}`);
    console.log(`   API: http://127.0.0.1:${PORT}/api/health\n`);
});
