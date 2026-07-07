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
        console.log("Setting up inputs...");
        await page.evaluate(() => {
            // Fill out forms so summary has data
            document.getElementById('f-name').value = 'John Doe';
            document.getElementById('f-city').value = 'Tel Aviv';
            document.getElementById('f-origin-city').value = 'Haifa';
            
            // Show modal and jump to summary
            document.getElementById('modal-overlay').classList.add('visible');
            document.getElementById('add-modal').classList.add('visible');
            
            showSummaryScreen(1, '4a');
        });
        
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'before_click.png' });
        
        console.log("Checking if btn-summary-feed-now is overlapping...");
        
        // This is the real test: simulate a REAL MOUSE CLICK
        // Puppeteer click uses real page coordinates, so if it's overlapped, it will throw an error or click the transparent div instead
        await page.click('#btn-summary-feed-now');
        console.log("Puppeteer click successful!");
        
        await page.waitForTimeout(1000);
        
        // Did we go to step 10 or recommendations?
        const currentActive = await page.evaluate(() => {
            const active = document.querySelector('.wizard-step.active');
            return active ? active.id : null;
        });
        console.log("Active step after click:", currentActive);
        
    } catch(err) {
        console.error("Test failed:", err.message);
    }
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
