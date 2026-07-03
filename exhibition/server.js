require('dotenv').config();
const express = require('express');
const path = require('path');
const { getDb } = require('./db/schema');

const app = express();
const PORT = process.env.PORT || 1337;

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', '*');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
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
app.get('/api/graph', (req, res) => {
    const db = getDb();
    const people = db.prepare('SELECT id, name, age, city, country, role, description, tags FROM people ORDER BY id').all();
    const connections = db.prepare(
        'SELECT person_a_id as source, person_b_id as target, type, strength FROM connections WHERE person_a_id < person_b_id'
    ).all();
    res.json({ people, connections });
});

// Health check
app.get('/api/health', (req, res) => {
    const db = getDb();
    const { count: people } = db.prepare('SELECT COUNT(*) as count FROM people').get();
    const { count: conns }  = db.prepare('SELECT COUNT(*) as count FROM connections WHERE person_a_id < person_b_id').get();
    res.json({ ok: true, people, connections: conns });
});

// Serve the visualization for any other route
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '127.0.0.1', () => {
    console.log(`\n🌐 Feed the Beast Exhibition running at http://127.0.0.1:${PORT}`);
    console.log(`   API: http://127.0.0.1:${PORT}/api/health\n`);
});
