class Storage extends Module {
	constructor(nav, name, abbr, parent = '', appData, slash) {
		super(nav, name, abbr, parent, undefined, undefined);

		this.appPath = appData;
		this.storagePath = this.appPath + `${slash}_custom${slash}storage${slash}`;

		let temp = {};
		let files = readDirectory(this.storagePath);
		for (let file of files) {
			if (file.match(/^\..*/g)) continue;

			let key = file.replace(/.json/g, '');
			temp[key] = JSON.parse(readFile(this.storagePath, key, 'json'))[key];
		}
		this.persistentStorage = temp;
		this.localStorage = {};
	}

	getContent() {
		let root = div('st');
		return root;
	}

	/* Storage-API */
	getAppPath() {
		return this.appPath;
	}

	getStoragePath() {
		return this.storagePath;
	}

	/**
	 * Equivalent to localStorage or sessionStorage
	 *
	 * @param {*} key
	 * @param {*} value
	 */
	setLocal(key, value) {
		this.localStorage[key] = value;
	}

	getLocal(key) {
		this.localStorage[key];
	}

	getAllLocal() {
		return this.localStorage;
	}

	clearLocal() {
		this.localStorage = {};
	}

	/**
	 * Equivalent to persistent storage
	 *
	 * @param {*} key
	 * @param {*} value
	 */
	set(key, value) {
		this.persistentStorage[key] = value;
		let kvp = {};
		kvp[key] = value;

		writeFile(this.storagePath, key, 'json', JSON.stringify(kvp));
	}

	get(key) {
		return this.persistentStorage[key];
	}

	getAll() {
		return this.persistentStorage;
	}

	clear() {
		this.persistentStorage = {};
	}
}

module.exports = Storage;
