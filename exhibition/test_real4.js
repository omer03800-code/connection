const puppeteer = require('puppeteer');
const { spawn } = require('child_process');

(async () => {
    const server = spawn('npm', ['run', 'start'], { cwd: '/Users/omerbarak/Documents/פגמר/exhibition' });
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('LOG:', msg.text()));
    
    // We want to see if the API call is made
    page.on('request', req => {
        if (req.url().includes('/api/')) console.log('REQ:', req.method(), req.url());
    });
    
    await page.goto('http://localhost:1337/');
    
    try {
        await page.waitForSelector('#btn-add-connection', { visible: true });
        await page.click('#btn-add-connection');
        
        await page.waitForSelector('#wizard-step-0.active', { visible: true });
        await page.type('#f-name-initial', 'John Doe Test');
        await page.keyboard.press('Enter');
        
        // Wait until summary is active
        // We will just expose a global function in the page context that can call showSummaryScreen
        await page.evaluate(() => {
            // we can't call showSummaryScreen directly.
            // But we can trigger the NEXT button of whatever is active
        });
        
        // Loop clicking next/skip until summary
        for(let i=0; i<15; i++) {
            await new Promise(r => setTimeout(r, 500));
            const activeStep = await page.evaluate(() => {
                const step = document.querySelector('.wizard-step.active');
                if (!step) return null;
                
                // If it's step 2 (scanning), wait
                if (step.id === 'wizard-step-2') return 'wait';
                
                // If it's summary, we're done
                if (step.id === 'wizard-step-summary') return 'summary';
                
                // Try to click skip
                const skipBtn = step.querySelector('.btn-skip');
                if (skipBtn) { skipBtn.click(); return 'skipped'; }
                
                // Try to click next
                const nextBtn = step.querySelector('.btn-next');
                if (nextBtn) { nextBtn.click(); return 'nexted'; }
                
                // Step 3 (match) ?
                const noBtn = step.querySelector('#btn-match-no');
                if (noBtn) { noBtn.click(); return 'noed'; }
                
                return 'stuck on ' + step.id;
            });
            console.log("Loop iteration", i, activeStep);
            if (activeStep === 'summary') break;
        }
        
        await page.waitForSelector('#wizard-step-summary.active', { visible: true });
        console.log("On summary step! Clicking [ FEED IT NOW ]");
        
        await page.click('#btn-summary-feed-now');
        await new Promise(r => setTimeout(r, 3000));
        
        const swalTitle = await page.evaluate(() => {
            return document.querySelector('.swal2-title') ? document.querySelector('.swal2-title').innerText : 'NO SWAL';
        });
        console.log("Swal title after click:", swalTitle);
        
    } catch(e) {
        console.error(e);
    }
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
