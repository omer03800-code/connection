const express = require('express');
const path = require('path');
const { getDb } = require('./db/schema');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// API routes
app.use('/api/people',      require('./routes/people'));
app.use('/api/connections', require('./routes/connections'));
app.use('/api/suggest',     require('./routes/suggest'));

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

app.listen(PORT, () => {
    console.log(`\n🌐 Six Degrees Exhibition running at http://localhost:${PORT}`);
    console.log(`   API: http://localhost:${PORT}/api/health\n`);
});
