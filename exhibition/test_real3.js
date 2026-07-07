const puppeteer = require('puppeteer');
const { spawn } = require('child_process');

(async () => {
    const server = spawn('npm', ['run', 'start'], { cwd: '/Users/omerbarak/Documents/פגמר/exhibition' });
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
    
    page.on('request', request => {
        if (request.url().includes('/api/')) {
            console.log('>> REQUEST:', request.method(), request.url());
        }
    });
    page.on('response', response => {
        if (response.url().includes('/api/')) {
            console.log('<< RESPONSE:', response.status(), response.url());
        }
    });

    await page.setViewport({ width: 1080, height: 1024 });
    await page.goto('http://localhost:1337/');
    
    try {
        console.log("Waiting for app to load...");
        await page.waitForSelector('#btn-add-connection', { visible: true });
        
        console.log("Clicking [ FEED THE BEAST ]");
        await page.click('#btn-add-connection');
        
        console.log("Waiting for Step 0...");
        await page.waitForSelector('#wizard-step-0.active', { visible: true });
        
        // Type name and press Enter
        await page.type('#f-name-initial', 'John Doe');
        await page.keyboard.press('Enter');
        
        console.log("Waiting for Step 2...");
        await page.waitForSelector('#wizard-step-2.active', { visible: true });
        
        // wait for simulation
        await new Promise(r => setTimeout(r, 2000));
        
        // now we should be on Step 4a or 1 or 3
        const activeStep = await page.evaluate(() => {
            const active = document.querySelector('.wizard-step.active');
            return active ? active.id : 'NONE';
        });
        console.log("Active step after search:", activeStep);
        
        // For John Doe, it probably goes to 4a because there are no matches.
        if (activeStep === 'wizard-step-4a') {
            await page.click('#wizard-step-4a .btn-next');
            await new Promise(r => setTimeout(r, 500));
        } else if (activeStep === 'wizard-step-3') {
            // Match found? click no
            await page.click('#btn-match-no');
            await new Promise(r => setTimeout(r, 500));
        }

        // Check if we are on step 1 (we should be if 4a -> next)
        const activeStep1 = await page.evaluate(() => document.querySelector('.wizard-step.active')?.id);
        console.log("Active step now:", activeStep1);
        
        if (activeStep1 === 'wizard-step-1') {
            // we already have the name, skip to 2
            await page.click('#wizard-step-1 .btn-next');
            await new Promise(r => setTimeout(r, 500));
            // step 2 is searching network again? No, after 1 comes 4 if role etc. Wait, the flow is complex.
        }
        
        // Let's just force the UI to summary
        console.log("Forcing summary step for testing...");
        await page.evaluate(() => {
            document.getElementById('f-name').value = 'John Doe';
            window.sessionNum = 1; // mock sessionNum
            // We can't call showSummaryScreen, but let's click the feed it now anyway?
            // Actually, we CANNOT force summary easily without showSummaryScreen.
            // Let's do it right. Let's see what step we're on and click "skip" or "next" until we hit summary.
        });
        
        for(let i=0; i<10; i++) {
            const stepId = await page.evaluate(() => document.querySelector('.wizard-step.active')?.id);
            if (stepId === 'wizard-step-summary') break;
            
            console.log("On step:", stepId);
            // Click skip if available, else next
            const hasSkip = await page.evaluate(() => !!document.querySelector('.wizard-step.active .btn-skip'));
            if (hasSkip) {
                await page.click('.wizard-step.active .btn-skip');
            } else {
                const hasNext = await page.evaluate(() => !!document.querySelector('.wizard-step.active .btn-next'));
                if (hasNext) await page.click('.wizard-step.active .btn-next');
                else break;
            }
            await new Promise(r => setTimeout(r, 500));
        }
        
        console.log("Waiting for Summary...");
        await page.waitForSelector('#wizard-step-summary.active', { visible: true });
        
        console.log("Clicking [ FEED IT NOW ] using native click()");
        await page.click('#btn-summary-feed-now');
        
        await new Promise(r => setTimeout(r, 2000));
        
        console.log("Checking result after click...");
        const swalTitle = await page.evaluate(() => {
            const el = document.querySelector('.swal2-title');
            return el ? el.innerText : 'NO SWAL';
        });
        console.log("Swal Title:", swalTitle);
        
    } catch(err) {
        console.error("Test failed:", err);
    }
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
