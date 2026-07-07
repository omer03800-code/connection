const puppeteer = require('puppeteer');
const { spawn } = require('child_process');

(async () => {
    const server = spawn('npm', ['run', 'start'], { cwd: '/Users/omerbarak/Documents/פגמר/exhibition' });
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    await page.setViewport({ width: 1080, height: 1024 });
    await page.goto('http://localhost:1337/');
    
    try {
        console.log("Waiting for app to load...");
        await page.waitForSelector('#btn-add-connection', { visible: true });
        
        console.log("Clicking [ FEED THE BEAST ]");
        await page.click('#btn-add-connection');
        
        console.log("Waiting for Step 0...");
        await page.waitForSelector('#wizard-step-0.active', { visible: true });
        await page.click('#wizard-step-0 .btn-next');
        
        console.log("Waiting for Step 1...");
        await page.waitForSelector('#wizard-step-1.active', { visible: true });
        await page.type('#f-name', 'John Doe');
        await page.click('#wizard-step-1 .btn-next');
        
        console.log("Waiting for Step 2...");
        await page.waitForSelector('#wizard-step-2.active', { visible: true });
        await page.click('#wizard-step-2 .btn-skip'); // skip age
        
        console.log("Waiting for Step 3...");
        await page.waitForSelector('#wizard-step-3.active', { visible: true });
        await page.click('#wizard-step-3 .btn-skip'); // skip role
        
        console.log("Waiting for Step 4...");
        await page.waitForSelector('#wizard-step-4.active', { visible: true });
        await page.click('#wizard-step-4 .btn-skip'); // skip cities
        
        console.log("Waiting for Summary...");
        await page.waitForSelector('#wizard-step-summary.active', { visible: true });
        
        console.log("Clicking [ FEED IT NOW ] using page.click()");
        try {
            await page.click('#btn-summary-feed-now');
            console.log("Puppeteer native click succeeded.");
        } catch(e) {
            console.error("Puppeteer native click failed!", e.message);
            console.log("Falling back to DOM click...");
            await page.evaluate(() => document.getElementById('btn-summary-feed-now').click());
        }
        
        await new Promise(r => setTimeout(r, 2000));
        
        console.log("Checking result after click...");
        const swalTitle = await page.evaluate(() => {
            const el = document.querySelector('.swal2-title');
            return el ? el.innerText : 'NO SWAL';
        });
        console.log("Swal Title:", swalTitle);
        
        const activeStep = await page.evaluate(() => {
            const active = document.querySelector('.wizard-step.active');
            return active ? active.id : 'NONE';
        });
        console.log("Active Wizard Step:", activeStep);
        
    } catch(err) {
        console.error("Test failed:", err);
    }
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
