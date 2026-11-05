// esegue motore.js in node come se fosse il Web Worker: node wrun.js '<messaggio JSON>'
const fs = require('fs'), vm = require('vm');
const msg = JSON.parse(process.argv[2]);
let res = null;
const ctx = { console, setTimeout, clearTimeout, Math, JSON, Date, Promise,
  postMessage: m => { if (m.type === 'result' || m.type === 'error') { res = m; console.log(JSON.stringify(m)); } } };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[3] || __dirname + '/motore.js', 'utf8') + '\n;this.__om = onmessage;', ctx);
ctx.__om({ data: msg });
