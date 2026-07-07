const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('public/index.html', 'utf-8');

// JSDOM mock
const dom = new JSDOM(html, { runScripts: 'dangerously', beforeParse(window) {
    window.Swal = { fire: () => Promise.resolve() };
    window.d3 = { select: () => ({ on: () => {} }), zoom: () => ({ on: () => {} }) };
} });
const window = dom.window;

window.addEventListener('error', event => {
  console.error("JSDOM Error:", event.error);
});

setTimeout(() => {
    try {
        const person = {
            id: 'p1',
            name: 'Test Person',
            tags: 'community:A',
            connections: [{id: 'p2', type: 'friend', strength: 4}]
        };
        window.people = [
            person,
            {id: 'p2', name: 'Other', role: 'Dev', city: 'TA'}
        ];
        
        window.openEditModal('edit', person);
        
        const list = window.document.getElementById('edit-connections-list');
        console.log("Connections generated:", list.children.length);
        if (list.children.length > 0) {
            console.log("Success! Inner HTML length:", list.innerHTML.length);
        } else {
            console.log("No connections generated!");
        }
    } catch (e) {
        console.error("Execution failed:", e);
    }
}, 500);

