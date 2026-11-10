// builds hsim.js: engine + simulator with DOM stubs, run directly by node (faster than vm)
const fs = require('fs');
const src = fs.readFileSync(__dirname + '/check.js', 'utf8').replace(/\ndealDecks\(\);\nrenderCatalog\(\);\nrender\(\);\s*$/, '\n');
const pre = `const noop=()=>{};const el=new Proxy({}, { get: (t, k) => k === 'value' ? '' : (typeof k === 'string' ? (t[k] ?? (() => el)) : undefined), set: () => true });
const document={addEventListener:noop,getElementById:()=>el,querySelector:()=>el,querySelectorAll:()=>[]};const window={};const localStorage={getItem:()=>null,setItem:noop};\n`;
fs.writeFileSync(__dirname + '/hsim.js', pre + src + '\n' + fs.readFileSync(__dirname + '/hmain.js', 'utf8'));
