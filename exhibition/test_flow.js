const puppeteer = require('puppeteer');
const { spawn } = require('child_process');
const path = require('path');

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
    await page.goto('http://localhost:3000/');
    
    try {
        console.log("Navigating to step 1...");
        // Start Add Wizard
        await page.click('.btn-nav'); // Assuming this opens the modal
        await page.waitForTimeout(1000);
        
        // Wait for step 1
        await page.waitForSelector('#wizard-step-1.active');
        await page.type('#f-name', 'John Doe');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        // Step 2
        await page.waitForSelector('#wizard-step-2.active');
        await page.type('#f-birth-year', '1990');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        // Step 3
        await page.waitForSelector('#wizard-step-3.active');
        await page.type('#f-role', 'Developer');
        await page.keyboard.press('Enter');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        // Step 4
        await page.waitForSelector('#wizard-step-4.active');
        await page.type('#f-origin-city', 'Haifa');
        await page.keyboard.press('Enter');
        await page.type('#f-city', 'Tel Aviv');
        await page.keyboard.press('Enter');
        await page.click('.btn-next');
        await page.waitForTimeout(500);
        
        // Step Summary
        await page.waitForSelector('#wizard-step-summary.active');
        console.log("Taking screenshot of summary screen...");
        await page.screenshot({ path: 'summary_screen.png' });
        
        console.log("Clicking Feed It Now...");
        // Use a standard click first to see if it works naturally
        await page.click('#btn-summary-feed-now');
        
        console.log("Waiting to see what happens...");
        await page.waitForTimeout(2000);
        await page.screenshot({ path: 'after_feed_it_now.png' });
        
        console.log("Done.");
    } catch(err) {
        console.error("Test failed:", err);
    }
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
