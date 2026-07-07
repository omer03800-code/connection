const puppeteer = require('puppeteer');
const { exec } = require('child_process');

(async () => {
    const server = exec('python3 -m http.server 8081 --directory public');
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    await page.goto('http://localhost:8081/index.html');
    await page.waitForSelector('#btn-summary-feed-now');
    
    await page.evaluate(() => {
        try {
            // Give nodes some data to match
            window.nodes = [
                {id: "1", name: "Bob", concepts: ["university:Haifa"]}
            ];
            document.getElementById('f-university').value = "Haifa";
            
            const btn = document.getElementById('btn-summary-feed-now');
            console.log("Clicking Feed It Now with matches...");
            btn.click();
        } catch(e) {
            console.error(e);
        }
    });
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    server.kill();
    await browser.close();
})();
