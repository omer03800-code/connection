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
        console.log("Evaluating processStep9 directly...");
        const result = await page.evaluate(() => {
            try {
                document.getElementById('f-name').value = 'John Doe';
                openModal('add');
                processStep9();
                return "SUCCESS";
            } catch(e) {
                return e.toString();
            }
        });
        
        console.log("Evaluate result:", result);
        
        await new Promise(r => setTimeout(r, 2000));
        
        const swalText = await page.evaluate(() => {
            const el = document.querySelector('.swal2-html-container');
            return el ? el.innerText : null;
        });
        console.log("Swal text:", swalText);
        
    } catch(err) {
        console.error("Test failed:", err.message);
    }
    
    server.kill();
    await browser.close();
    process.exit(0);
})();
