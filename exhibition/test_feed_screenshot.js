const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    // Set viewport to a typical desktop size
    await page.setViewport({ width: 1280, height: 800 });
    
    await page.goto('http://localhost:1337/');
    await page.waitForSelector('#btn-add-connection', { visible: true });
    
    await page.evaluate(() => { document.getElementById('btn-add-connection').click(); });
    await new Promise(r => setTimeout(r, 500));
    
    await page.evaluate(() => {
        document.getElementById('f-name-initial').value = 'Test User';
        document.getElementById('btn-wizard-global-next').click();
    });
    
    await new Promise(r => setTimeout(r, 500));
    await page.evaluate(() => {
        document.getElementById('f-birth-year').value = '1990';
        document.getElementById('btn-wizard-global-next').click();
    });
    
    await new Promise(r => setTimeout(r, 500));
    await page.evaluate(() => {
        document.getElementById('f-city').value = 'Tel Aviv';
        document.getElementById('btn-wizard-global-next').click();
    });
    
    await new Promise(r => setTimeout(r, 500));
    await page.evaluate(() => {
        document.getElementById('btn-wizard-global-next').click();
    });
    
    await new Promise(r => setTimeout(r, 500));
    
    // Take screenshot BEFORE clicking
    await page.screenshot({ path: 'before_feed_now.png' });
    
    await page.evaluate(() => {
        document.getElementById('btn-summary-feed-now').click();
    });
    
    await new Promise(r => setTimeout(r, 1000));
    
    // Take screenshot AFTER clicking
    await page.screenshot({ path: 'after_feed_now.png' });
    
    await browser.close();
    process.exit(0);
})();
