const puppeteer = require('puppeteer');
const { spawn } = require('child_process');

(async () => {
    const server = spawn('npm', ['run', 'start'], { cwd: '/Users/omerbarak/Documents/פגמר/exhibition' });
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('LOG:', msg.text()));
    page.on('pageerror', err => console.log('ERROR:', err.toString()));
    
    await page.goto('http://localhost:1337/');
    await page.waitForSelector('#btn-add-connection', { visible: true });
    
    await page.evaluate(() => {
        // Mock values so generateRecommendations doesn't crash on missing required inputs
        document.getElementById('form-mode').value = 'add';
        document.getElementById('f-name-initial').value = 'Test User';
        document.getElementById('f-name').value = 'Test User';
        document.getElementById('f-birth-year').value = '1990';
        document.getElementById('f-city').value = 'Tel Aviv';
        
        // Let's call triggerRecommendations with true
        try {
            console.log("Calling triggerRecommendations");
            triggerRecommendations(1, true);
            console.log("Called successfully");
        } catch(e) {
            console.error("triggerRecommendations crashed:", e);
        }
    });
    
    await new Promise(r => setTimeout(r, 2000));
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
