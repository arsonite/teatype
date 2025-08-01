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

	//mainWindow.setMenu(null);

	//mainWindow.webContents.openDevTools()

	mainWindow.on('closed', function() {
		globalShortcut.unregisterAll();
	});
}

app.on('ready', () => {
	createWindow();

	/* Custom shortcuts */
	globalShortcut.register('Shift+Command+R', () => {
		mainWindow.setSize(STANDARD_WIDTH, STANDARD_HEIGHT);
	});

	globalShortcut.register('Shift+Ctrl+R', () => {
		mainWindow.setSize(STANDARD_WIDTH, STANDARD_HEIGHT);
	});

	globalShortcut.register('Ctrl+R', () => {
		return;
	});

	globalShortcut.register('F5', () => {
		return;
	});

	/*globalShortcut.register('alt+Command+I', () => {
    return;
  });*/
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

app.on('activate', () => {
	if (mainWindow === null) {
		createWindow();
	}
});

app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
