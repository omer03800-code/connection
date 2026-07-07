const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('LOG:', msg.text()));
    page.on('pageerror', err => console.log('ERROR:', err.toString()));
    
    await page.goto('http://localhost:1337/');
    await page.waitForSelector('#btn-add-connection', { visible: true });
    
    // Fill out initial form and start wizard
    await page.evaluate(() => {
        document.getElementById('form-mode').value = 'add';
        document.getElementById('f-name-initial').value = 'Test User';
        document.getElementById('f-name').value = 'Test User';
        document.getElementById('f-birth-year').value = '1990';
        // Go to step 4
        goToWizardStep('4');
    });
    
    // Wait a bit, then click [ CONTINUE ] to go to Summary Screen
    await new Promise(r => setTimeout(r, 500));
    await page.evaluate(() => {
        document.getElementById('btn-wizard-global-next').click();
    });
    
    // Wait for Summary Screen
    await new Promise(r => setTimeout(r, 500));
    
    // Click [ FEED IT NOW ]
    console.log("CLICKING FEED IT NOW");
    await page.evaluate(() => {
        const btn = document.getElementById('btn-summary-feed-now');
        if (!btn) console.log("BUTTON NOT FOUND");
        else btn.click();
    });
    
    await new Promise(r => setTimeout(r, 1000));
    await browser.close();
    process.exit(0);
})();
