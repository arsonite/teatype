class Logger {
	constructor() {
		this.scriptName = '';
	}

	setScriptName(scriptName) {
		this.scriptName = scriptName;
	}

	debug(msg) {
		let date = new Date();
		console.log(
			date.getHours() +
				':' +
				date.getMinutes() +
				':' +
				date.getSeconds() +
				date.getMilliseconds() +
				'|' +
				this.scriptName +
				': ' +
				msg
		);
	}

	debugLS(msg) {
		debug(msg);
		let log = localStorage.getItem('log');
		log += '\n' + msg;
		localStorage.setItem('log', log);
	}

	info(msg) {
		console.log(this.scriptName + ': ' + msg);
	}

	console(msg) {
		console.log(msg);
	}
}

module.exports = Logger;
