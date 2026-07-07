const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    // We will serve the file via a local http server to avoid CORS issues
    const { exec } = require('child_process');
    const server = exec('npx http-server public -p 8081');
    
    await new Promise(resolve => setTimeout(resolve, 2000)); // wait for server
    
    await page.goto('http://localhost:8081/index.html');
    
    // Wait for the DOM and scripts to settle
    await page.waitForTimeout(1000);
    
    await page.evaluate(() => {
        try {
            // Mock data so generateRecommendations doesn't return false
            window.nodes = [{id: "1", name: "Test Person"}];
            // Simulate that we typed "Test" in some fields
            document.getElementById('f-city').value = "Test";
            document.getElementById('f-origin-city').value = "Test";
            
            const btn = document.getElementById('btn-summary-feed-now');
            if (btn) {
                console.log("Clicking Feed It Now...");
                btn.click();
            } else {
                console.log("Button not found");
            }
        } catch(e) {
            console.error(e);
        }
    });
    
    await page.waitForTimeout(1000);
    
    server.kill();
    await browser.close();
})();
