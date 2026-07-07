const fs = require('fs');
const html = fs.readFileSync('public/index.html', 'utf-8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
let js = scriptMatch[1];

// mock global variables
global.document = {
    addEventListener: () => {},
    getElementById: (id) => ({
        value: '',
        style: {},
        classList: { add: ()=>{}, remove: ()=>{}, contains: ()=>true },
        innerHTML: '',
        addEventListener: () => {},
        appendChild: () => {},
        prepend: () => {},
        children: [],
        querySelector: () => null,
        querySelectorAll: () => []
    }),
    createElement: () => ({
        style: {},
        classList: { add: ()=>{}, remove: ()=>{}, contains: ()=>false },
        innerHTML: '',
        addEventListener: () => {},
        querySelector: () => ({ style: {}, addEventListener: ()=>{}, classList: { add: ()=>{}, remove: ()=>{} }, querySelector: ()=>({ textContent: '' }) }),
        querySelectorAll: () => []
    }),
    querySelectorAll: () => []
};
global.window = global;
global.people = [ { id: 'p1', name: 'A', tags: '', connections: [ { id: 'p2', type: 'friend', strength: 3 } ] }, { id: 'p2', name: 'B', tags: '', connections: [] } ];
global.userNames = ['A', 'B'];

try {
    eval(js);
    console.log("Parsed OK!");
    
    // Now trigger openEditModal
    openEditModal(global.people[0]);
    console.log("openEditModal OK!");
    
} catch (e) {
    console.error("Eval error:", e);
}
