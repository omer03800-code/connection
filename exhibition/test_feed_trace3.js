const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('LOG:', msg.text()));
    page.on('pageerror', err => console.log('ERROR:', err.toString()));
    
    await page.goto('http://localhost:1337/');
    await page.waitForSelector('#btn-add-connection', { visible: true });
    
    await page.evaluate(() => {
        document.getElementById('btn-add-connection').click();
    });
    
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
    await page.evaluate(() => {
        console.log("Clicking Feed It Now...");
        const btn = document.getElementById('btn-summary-feed-now');
        if (btn) btn.click();
        else console.log("Feed It Now btn not found");
    });
    
    await new Promise(r => setTimeout(r, 500));
    
    const visibleStep = await page.evaluate(() => {
        return document.querySelector('.wizard-step.active')?.id;
    });
    console.log("Active step after click:", visibleStep);

    await browser.close();
    process.exit(0);
})();
