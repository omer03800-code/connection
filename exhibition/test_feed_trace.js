const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('LOG:', msg.text()));
    page.on('pageerror', err => console.log('ERROR:', err.toString()));
    
    await page.goto('http://localhost:1337/');
    await page.waitForSelector('#btn-add-connection', { visible: true });
    
    await page.evaluate(() => {
        document.getElementById('form-mode').value = 'add';
        goToWizardStep('summary'); // Directly show summary
    });
    
    await new Promise(r => setTimeout(r, 500));
    
    const visibleStep = await page.evaluate(() => {
        return document.querySelector('.wizard-step.active')?.id;
    });
    console.log("Active step before click:", visibleStep);
    
    await page.evaluate(() => {
        console.log("Clicking button...");
        document.getElementById('btn-summary-feed-now').click();
    });
    
    await new Promise(r => setTimeout(r, 500));
    
    const visibleStepAfter = await page.evaluate(() => {
        return document.querySelector('.wizard-step.active')?.id;
    });
    console.log("Active step after click:", visibleStepAfter);
    
    const displayStyle = await page.evaluate(() => {
        return document.getElementById('wizard-step-rec')?.style.display;
    });
    console.log("Rec step display:", displayStyle);

    await browser.close();
    process.exit(0);
})();
