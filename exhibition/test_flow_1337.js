const puppeteer = require('puppeteer');
const { spawn } = require('child_process');

(async () => {
    console.log("Starting server...");
    const server = spawn('npm', ['run', 'start'], { cwd: '/Users/omerbarak/Documents/פגמר/exhibition' });
    
    await new Promise(resolve => setTimeout(resolve, 3000));
    console.log("Server started. Launching browser...");
    
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    await page.setViewport({ width: 1080, height: 1024 });
    await page.goto('http://localhost:1337/');
    
    try {
        console.log("Navigating to step 1...");
        // Start Add Wizard
        await page.click('.btn-nav');
        await page.waitForTimeout(1000);
        
        await page.waitForSelector('#wizard-step-1.active');
        await page.type('#f-name', 'John Doe');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        await page.waitForSelector('#wizard-step-2.active');
        await page.type('#f-birth-year', '1990');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        await page.waitForSelector('#wizard-step-3.active');
        await page.type('#f-role', 'Developer');
        await page.keyboard.press('Enter');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        await page.waitForSelector('#wizard-step-4.active');
        await page.type('#f-origin-city', 'Haifa');
        await page.keyboard.press('Enter');
        await page.type('#f-city', 'Tel Aviv');
        await page.keyboard.press('Enter');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        await page.waitForSelector('#wizard-step-summary.active');
        
        console.log("Clicking Feed It Now...");
        
        // Wait specifically for the button to be in DOM
        await page.waitForSelector('#btn-summary-feed-now');
        
        // Use page.evaluate to see if click actually triggers
        const clicked = await page.evaluate(() => {
            let wasClicked = false;
            const btn = document.getElementById('btn-summary-feed-now');
            btn.addEventListener('click', () => { wasClicked = true; });
            return new Promise(resolve => {
                btn.click(); // DOM native click
                setTimeout(() => resolve(wasClicked), 100);
            });
        });
        
        console.log("Did DOM click work?:", clicked);
        
        // Let's also test Puppeteer's click which uses coordinate events
        await page.click('#btn-summary-feed-now');
        
        await page.waitForTimeout(2000);
        console.log("Done.");
    } catch(err) {
        console.error("Test failed:", err);
    }
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
