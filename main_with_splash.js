const { app, BrowserWindow, globalShortcut } = require('electron');
const controller = require('electron').ipcMain;

const path = require('path');
const url = require('url');

const MIN_WINDOW_HEIGHT = 600;
const MIN_WINDOW_WIDTH = 720;

const STANDARD_HEIGHT = 650;
const STANDARD_WIDTH = 850;

let mainWindow;

process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = true;

controller.on('reply', (event, message) => {
	mainWindow.webContents.send(
		'messageFromMain',
		`This is the message from the second window: ${message}`
	);
});

function createWindow() {
	mainWindow = new BrowserWindow({
		titleBarStyle: 'hidden',

		minHeight: MIN_WINDOW_HEIGHT,
		minWidth: MIN_WINDOW_WIDTH,

		height: STANDARD_HEIGHT,
		width: STANDARD_WIDTH,

		webPreferences: {
			experimentalFeatures: true
		}
	});

	mainWindow.loadURL(
		url.format({
			pathname: path.join(__dirname, 'hub.html'),
			protocol: 'file:',
			slashes: true
		})
	);

	//mainWindow.webContents.openDevTools()

	mainWindow.on('closed', function() {
		globalShortcut.unregisterAll();

		let tempURL =
			'/Users/burak/Desktop/Projekte/Coding/Web-Entwicklung/Electron/TeaType-Collection/src/db/';

		let temp = require('fs');
		temp.writeFile(tempURL + 'splash_boolean.txt', 'false', 'utf8', err => {
			if (err) throw err;
		});
	});
}

app.on('ready', () => {
	createWindow();

	/* Logging correct paths */
	console.log(app.getAppPath());
	console.log(app.getPath('appData'));
	console.log(app.getPath('userData'));

	/* Custom shortcuts */
	/*const ret = globalShortcut.register('Command+R', () => {
    mainWindow.setSize(STANDARD_WIDTH, STANDARD_HEIGHT);
  });*/

	/*const ret2 = globalShortcut.register('alt+Command+I', () => {
    return;
  });*/
});

app.on('window-all-closed', function() {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

app.on('activate', function() {
	if (mainWindow === null) {
		createWindow();
	}
});

app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
