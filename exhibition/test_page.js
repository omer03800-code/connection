const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.error('PAGE ERROR:', error.message));
  
  await page.goto('http://localhost:3000');
  await page.waitForTimeout(2000);
  
  // click an edit button or trigger openEditPersonOverlay
  await page.evaluate(() => {
    if (typeof openModal === 'function') {
      openModal('edit', people[0]);
    }
  });
  
  await page.waitForTimeout(500);
  await browser.close();
})();
