const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    await page.goto('file://' + path.resolve('public/index.html'));
    
    // Attempt to trigger the feed now logic
    await page.evaluate(() => {
        try {
            // Need to set up basic mock state
            window._connections = [];
            window.nodes = [];
            
            // Assume sessionNum = 1
            const btn = document.getElementById('btn-summary-feed-now');
            if (btn) {
                // mock the onclick assignment since we don't naturally reach here
                btn.onclick = () => triggerRecommendations(1, true);
                btn.click();
            } else {
                console.log("Button not found");
            }
        } catch(e) {
            console.error(e);
        }
    });
    
    setTimeout(async () => {
        await browser.close();
    }, 1000);
})();
