const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM, VirtualConsole } = jsdom;

const virtualConsole = new VirtualConsole();
virtualConsole.on("jsdomError", (error) => {
  console.error(error.stack, error.detail);
});
virtualConsole.on("error", (error) => {
  console.error("error:", error);
});

const html = fs.readFileSync('public/index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: "dangerously", virtualConsole });

