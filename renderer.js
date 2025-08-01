const remoteWindow = require('electron').remote.BrowserWindow;
const receiver = require('electron').ipcRenderer;

let lg = new Logger();

let dmeWindow;
let dmeWindowCreated = false;

let domWindow;
let domWindowCreated = false;

let logWindow;
let logWindowCreated = false;

let classKey = '';

function createDmeWindow() {
	dmeWindow = new remoteWindow({
		width: 1200,
		height: 700,
		transparent: true,
		frame: false,

		webPreferences: {
			experimentalFeatures: true
		}
	});

	dmeWindow.setResizable(false);

	dmeWindow.loadURL(
		url.format({
			pathname: path.join(absoluteURL, 'window_modules/dme/frame.html'),
			protocol: 'file:',
			slashes: true
		})
	);

	dmeWindowCreated = true;

	dmeWindow.on('closed', () => {
		dmeWindowCreated = false;
		dmeWindow = null;
	});
}

function createDomWindow() {
	domWindow = new remoteWindow({
		titleBarStyle: 'hidden',
		width: 720,
		height: 600
	});

	domWindow.setResizable(false);

	domWindow.loadURL(
		url.format({
			pathname: path.join(absoluteURL, 'window_modules/dom/dom.html'),
			protocol: 'file:',
			slashes: true
		})
	);

	domWindowCreated = true;

	domWindow.on('closed', () => {
		domWindowCreated = false;
		domWindow = null;
	});
}

function createLogWindow() {
	logWindow = new remoteWindow({
		titleBarStyle: 'hidden',
		width: 720,
		height: 600
	});

	logWindow.setResizable(false);

	logWindow.loadURL(
		url.format({
			pathname: path.join(absoluteURL, 'window_modules/log/log.html'),
			protocol: 'file:',
			slashes: true
		})
	);

	logWindow = true;

	logWindow.on('closed', () => {
		logWindow = false;
		logWindow = null;
	});
}

receiver.on('messageFromMain', (event, message) => {
	//console.log(`This is the message from the second window sent via main: ${message}`);
});

function sendDOM() {
	if (!domWindowCreated) {
		return;
	}
	domWindow.webContents.send('dom', document.documentElement.outerHTML);
}

function sendLog() {}

function log(msg) {
	lg.debug(msg);
}
lg.setScriptName('renderer.js');

/* Seperate multiple classes */
function seperateHTMLClasses(classes) {
	return classes.split(' ');
}

/* Disables any kind of user-based zooming */
let webFrame = require('electron').webFrame;
webFrame.setZoomFactor(1);
webFrame.setVisualZoomLevelLimits(1, 1);
webFrame.setLayoutZoomLevelLimits(0, 0);

/* RGB-To-Hex */
function componentToHex(c) {
	let hex = c.toString(16);
	if (hex.length == 1) {
		return '0' + hex;
	}
	return hex;
	//return hex.length == 1 ? "0" + hex : hex;
}

function RGBtoHex(r, g, b) {
	return '#' + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

/* Hex-To-RGB */
function hexToRGB(hex) {
	let shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
	hex = hex.replace(shorthandRegex, (m, r, g, b) => {
		return r + r + g + g + b + b;
	});

	let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	return result
		? {
				r: parseInt(result[1], 16),
				g: parseInt(result[2], 16),
				b: parseInt(result[3], 16)
		  }
		: null;
}

/* Color functions */
function brightenHex(hex, factor) {
	let rgb = hexToRGB(hex);
	rgb.b += factor;
	rgb.g += factor;
	rgb.r += factor;
	rgb = RGBtoHex(rgb);
	return rgb;
}

function darkenHex(hex, factor) {}

function brightenRGB(rgb, factor) {}

function darkenRGB(rgb, factor) {}
