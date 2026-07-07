const puppeteer = require('puppeteer');
const { spawn } = require('child_process');

(async () => {
    const server = spawn('npm', ['run', 'start'], { cwd: '/Users/omerbarak/Documents/פגמר/exhibition' });
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('LOG:', msg.text()));
    page.on('pageerror', err => console.log('ERROR:', err.toString()));
    page.on('request', req => { if (req.url().includes('/api/')) console.log('REQ:', req.method(), req.url()); });
    
    await page.goto('http://localhost:1337/');
    await page.waitForSelector('#btn-add-connection', { visible: true });
    
    await page.evaluate(() => {
        // Mock all values needed for generateRecommendations
        document.getElementById('form-mode').value = 'add';
        document.getElementById('f-name-initial').value = 'Test User';
        document.getElementById('f-name').value = 'Test User';
        document.getElementById('f-birth-year').value = '1990';
        document.getElementById('f-city').value = 'Tel Aviv';
        
        // Let's manually set onclick on something inside scope? We can't.
        // BUT btn-summary-feed-now already HAS its onclick attached inside showSummaryScreen!
        // We can't call showSummaryScreen directly, so btn-summary-feed-now doesn't have its onclick assigned yet!
    });
    
    await new Promise(r => setTimeout(r, 1000));
    server.kill();
    await browser.close();
    process.exit(0);
})();
