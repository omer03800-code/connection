const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    page.on('request', request => {
        if (request.url().includes('/api/')) {
            console.log('>> REQUEST:', request.method(), request.url(), request.postData());
        }
    });
    
    page.on('response', async response => {
        if (response.url().includes('/api/')) {
            console.log('<< RESPONSE:', response.status(), response.url());
            try {
                console.log('   BODY:', await response.text());
            } catch(e) {}
        }
    });
    
    await page.setViewport({ width: 1080, height: 1024 });
    await page.goto('http://localhost:1337/');
    
    try {
        console.log("Setting up inputs...");
        await page.evaluate(() => {
            document.getElementById('f-name').value = 'John Doe';
            openModal('add');
            goToWizardStep('summary');
        });
        
        await page.waitForTimeout(1000);
        
        console.log("Clicking btn-summary-feed-now in DOM...");
        
        const clicked = await page.evaluate(() => {
            let wasClicked = false;
            const btn = document.getElementById('btn-summary-feed-now');
            btn.addEventListener('click', () => { wasClicked = true; });
            btn.click();
            return wasClicked;
        });
        
        console.log("Did DOM click work?:", clicked);
        
        await page.waitForTimeout(2000);
        
        const swalText = await page.evaluate(() => {
            const el = document.querySelector('.swal2-html-container');
            return el ? el.innerText : null;
        });
        console.log("Swal text:", swalText);
        
    } catch(err) {
        console.error("Test failed:", err.message);
    }
    
    await browser.close();
    process.exit(0);
})();
