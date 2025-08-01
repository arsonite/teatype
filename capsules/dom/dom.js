/* Disables any kind of user-based zooming */
let webFrame = require('electron').webFrame;
webFrame.setZoomFactor(1);
webFrame.setVisualZoomLevelLimits(1, 1);
webFrame.setLayoutZoomLevelLimits(0, 0);

let sender = require('electron').ipcRenderer;
sender.on('dom', (event, dom) => { 
    parseDOM(dom);
});

let DOM = '';
let out_dom;

function showDOM() {
    //sender.send('reply', `Send message from second window to renderer via main.`);
    out_dom.value = DOM;
}

function parseDOM(dom) {
    DOM = dom.trim().replace(/\<\!\-\-\s.*\-\-\>\s+/g, '');
    showDOM();
}

document.addEventListener('DOMContentLoaded', () => {
    out_dom = document.getElementById('out_dom');
});