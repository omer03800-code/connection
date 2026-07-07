const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('LOG:', msg.text()));
    page.on('pageerror', err => console.log('ERROR:', err.toString()));
    
    await page.goto('http://localhost:1337/');
    await page.waitForSelector('#btn-add-connection', { visible: true });
    
    // Evaluate to run the exact logic that normally happens
    await page.evaluate(() => {
        // Mock data
        document.getElementById('form-mode').value = 'add';
        document.getElementById('f-name-initial').value = 'Test User';
        document.getElementById('f-name').value = 'Test User';
        document.getElementById('f-birth-year').value = '1990';
        
        // This simulates reaching step 4a and clicking NEXT
        showSummaryScreen(1, '4a');
    });
    
    await new Promise(r => setTimeout(r, 500));
    
    await page.evaluate(() => {
        console.log("Clicking Feed It Now...");
        document.getElementById('btn-summary-feed-now').click();
    });
    
    await new Promise(r => setTimeout(r, 500));
    
    const visibleStep = await page.evaluate(() => {
        return document.querySelector('.wizard-step.active')?.id;
    });
    console.log("Active step after click:", visibleStep);

    await browser.close();
    process.exit(0);
})();
