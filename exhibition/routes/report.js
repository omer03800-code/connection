const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const nodemailer = require('nodemailer');

// Ensure reports directory exists for local logging
const reportsDir = path.join(__dirname, '..', 'reports');
if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
}

// Configure nodemailer transporter
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER || 'omer03800@gmail.com',
        pass: process.env.EMAIL_PASS || 'your_gmail_app_password_here' 
    }
});

router.post('/', async (req, res) => {
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

    // Save to a local file for persistence
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
        
        const mailOptions = {
            from: process.env.EMAIL_USER || 'omer03800@gmail.com',
            to: 'omer03800@gmail.com',
            subject: `New Report: ${personName}`,
            text: `A new report has been submitted.\n\nTarget: ${personName} (ID: ${personId})\nReason: ${reason}\nExplanation: ${explanation || 'None provided'}\nTimestamp: ${timestamp}\n`
        };

        try {
            await transporter.sendMail(mailOptions);
            console.log(`📧 Email sent successfully to omer03800@gmail.com`);
        } catch (emailErr) {
            console.error('⚠️ Failed to send email (Please set EMAIL_USER and EMAIL_PASS environment variables):', emailErr.message);
        }

        res.status(200).json({ success: true, message: 'Report received' });
    } catch (err) {
        console.error('Failed to process report:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
