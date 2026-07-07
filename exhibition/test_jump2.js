const puppeteer = require('puppeteer');

(async () => {
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
            openModal('add');
            goToWizardStep('summary');
        });
        
        await page.waitForTimeout(1000);
        await page.screenshot({ path: 'before_click.png' });
        
        console.log("Checking if btn-summary-feed-now is overlapping...");
        
        const clicked = await page.evaluate(() => {
            let wasClicked = false;
            const btn = document.getElementById('btn-summary-feed-now');
            btn.addEventListener('click', () => { wasClicked = true; });
            btn.click();
            return wasClicked;
        });
        
        console.log("Did DOM click work?:", clicked);
        
        await page.waitForTimeout(1000);
        
        // Did we go to step 10 or recommendations?
        const currentActive = await page.evaluate(() => {
            const active = document.querySelector('.wizard-step.active');
            return active ? active.id : null;
        });
        console.log("Active step after click:", currentActive);
        
        // Check if there is an error Swal
        const swalText = await page.evaluate(() => {
            const el = document.querySelector('.swal2-html-container');
            return el ? el.innerText : null;
        });
        console.log("Swal text:", swalText);
        
        await page.screenshot({ path: 'after_click.png' });
        
    } catch(err) {
        console.error("Test failed:", err.message);
    }
    
    await browser.close();
    process.exit(0);
})();
