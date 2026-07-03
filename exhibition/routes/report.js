const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

// Ensure reports directory exists for local logging
const reportsDir = path.join(__dirname, '..', 'reports');
if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
}

router.post('/', (req, res) => {
    const { personId, personName, reason, explanation } = req.body;

    if (!personId || !reason) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    const timestamp = new Date().toISOString();
    
    // Log to console
    console.log(`\n================ REPORT RECEIVED ================`);
    console.log(`Time:        ${timestamp}`);
    console.log(`Target:      ${personName} (ID: ${personId})`);
    console.log(`Reason:      ${reason}`);
    console.log(`Explanation: ${explanation || 'N/A'}`);
    console.log(`=================================================\n`);

    // Save to a local file for persistence (easy to switch to SMTP later)
    const reportData = {
        timestamp,
        personId,
        personName,
        reason,
        explanation
    };

    const filename = `report_${Date.now()}_${personId}.json`;
    const filepath = path.join(reportsDir, filename);
    
    try {
        fs.writeFileSync(filepath, JSON.stringify(reportData, null, 2));
        res.status(200).json({ success: true, message: 'Report received' });
    } catch (err) {
        console.error('Failed to write report to disk:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
