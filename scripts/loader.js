class Loader {
	constructor(path) {
		/* Temporary imports */
		const { app } = require('electron').remote;
		this.appPath = app.getPath('userData');
		console.log(this.appPath);
		this.storagePath = this.appPath + '/_custom/' + path;

		let temp = {};

		const iterate = filename => {
			const fs = require('fs');
			const path = require('path');

			let file = fs.lstatSync(filename),
				info = {
					path: filename,
					name: path.basename(filename)
				};

			if (file.isDirectory()) {
				info[info.name] = fs.readdirSync(filename).map(function(child) {
					return iterate(filename + '/' + child);
				});
			} else {
				info.name = JSON.parse(fs.readFileSync(info.path, 'utf8'));
			}

			return info;
		};

		const create = key => {};

		let foo = iterate(this.storagePath);
		console.log(foo);

		this.localStorage = temp;
	}

	/* Storage-API */
	getAppPath() {
		return this.appPath;
		/*
		let extendedPath = this.storagePath;
		let files = fs.readdirSync(this.storagePath);
		 Recursive directory to json 
		let iterate = (file, depth = 0) => {
			if (Array.isArray(file)) {
				file.forEach(f => {
					iterate(f, depth++);
				});
				return;
			} else if (file.contains('.json')) {
				extendedPath += file;
				let foo = fs.readFileSync(extendedPath, 'utf8');
				console.log(foo);
			} else {
				iterate(file);
			}
		};
		iterate(files);
		*/
		let files = readDirectory(this.storagePath);
		for (let file of files) {
			console.log(files);
			if (file.match(/^\..*/g)) continue;
			let key = file.replace(/.json/g, '');
			temp[key] = JSON.parse(readFile(this.storagePath, key, 'json'))[key];
		}
	}

	getStoragePath() {
		return this.storagePath;
	}

	/**
	 * Equivalent to localStorage or sessionStorage.
	 *
	 * @param {*} key
	 * @param {*} value
	 */
	set(key, value) {
		this.localStorage[key] = value;
	}

	get(key) {
		this.localStorage[key];
	}

	getAll() {
		return this.localStorage;
	}

	clear() {
		this.localStorage = {};
	}
}

module.exports = Loader;

/* TODO: Wrap plain text into variables to eliminate need for DOM-parsing */
/*
let out_ls_key, out_ls_val, in_ls;
let hr;
let form_ls;
let label_container;
let check_unit;

function localstorage_WRAPPER() {

    hr = d.create('hr');
    hr.className = 'vertical';
    d.insertAfter(left_container, hr);

    form_ls = d.form;
    form_ls.className = 'form_ls';

    right_container.append(form_ls);

    label_container = d.create('label');
    label_container.className = 'container';

    check_unit = d.create('input');
    check_unit.type = 'radio';
    check_unit.id = 'check_unit';
    check_unit.checked = true;
    check_unit.name = 'radio';
    
    span_unit = d.create('span');
    
    sendDOM();
}
*/

function home_ls_HTML() {
	main_header.innerHTML =
		n2 + '<p id="p1">Home </p>' + n2 + '<p id="p2">localStorage</p>' + n1;

	left_container.innerHTML =
		n1 +
		'<ul id="out_ls_key"></ul>' +
		n +
		'<textarea id="out_ls_val" rows="18" cols="35" readonly></textarea>' +
		n +
		'<textarea id="in_ls" rows="18" cols="35"></textarea>';

	right_container.innerHTML =
		'<form class="form_ls">' +
		'<label class="container">Unit' +
		'<input type="radio" id="check_unit" checked="checked" name="radio">' +
		'<span class="checkmark"></span>' +
		'</label>' +
		'<label class="container">Array' +
		'<input type="radio" id="check_array" name="radio">' +
		'<span class="checkmark"></span>' +
		'</label>' +
		'<label class="container_check">Regex' +
		'<input type="checkbox" id="check_regex" disabled>' +
		'<span class="checkmark"></span>' +
		'</label>' +
		'<input type="text" id="in_seperator" placeholder="Array-Seperator" disabled>' +
		'</form>' +
		'<hr class=">' +
		'<form class="form_ls">' +
		'<label class="container">Raw Data' +
		'<input type="radio" id="check_data" checked="checked" name="radio">' +
		'<span class="checkmark"></span>' +
		'</label>' +
		'<label class="container">JSON' +
		'<input type="radio" id="check_json" name="radio">' +
		'<span class="checkmark"></span>' +
		'</label>' +
		'<label class="container">Storage' +
		'<input type="radio" id="check_storage" name="radio">' +
		'<span class="checkmark"></span>' +
		'</label>' +
		'</form>' +
		'<hr>' +
		'<form id="form_names" class="form_ls">' +
		'<input type="text" id="in_key" placeholder="Key">' +
		'</form>' +
		'<form class="form_ls">' +
		'<button type="button" id="store">Store</button>' +
		'<button type="button" id="emptyAll">Empty All</button>' +
		'</form>';

	home_ls_functions();
}

function home_ls_functions() {
	let storeButton = $('#store')[0];
	let emptyButton = $('#emptyAll')[0];

	let in_ls = $('#in_ls')[0];
	let in_key = $('#in_key')[0];

	let out_ls_val = $('#out_ls_val')[0];
	let out_ls_key = $('#out_ls_key')[0];

	let in_seperator = $('#in_seperator')[0];

	let check_unit = $('#check_unit')[0];
	let check_array = $('#check_array')[0];
	let check_regex = $('#check_regex')[0];
	let regex = false;

	let check_data = $('#check_data')[0];
	let check_json = $('#check_json')[0];
	let check_storage = $('#check_storage')[0];

	////////// onClick-Events //////////

	check_unit.onclick = function() {
		in_seperator.disabled = true;
		check_regex.disabled = true;
		check_regex.checked = false;
		check_regex.parentElement.style.color = '#666';
	};

	check_array.onclick = function() {
		in_seperator.disabled = false;
		check_regex.disabled = false;
		check_regex.parentElement.style.color = '#FFF';
	};
	check_regex.parentElement.style.color = '#666';

	check_regex.onchange = function() {
		regex = check_regex.checked;
	};

	storeButton.onclick = function() {
		let val = in_ls.value;
		let key = in_key.value;

		if (val === '' || key === '') {
			alert('error', 'No empty strings allowed!');
			return;
		}

		if (!in_seperator.disabled) {
			let seperator = in_seperator.value;
			if (regex) {
				if (seperator === '\\n') {
					val = JSON.stringify(val.split(/\n/));
				} else {
					val = JSON.stringify(val.split(/ / + seperator + / /));
				}
			} else {
				val = JSON.stringify(val.split(seperator));
			}
		}

		localStorage.setItem(key, val);
		alert(
			'success',
			'Key-value pair ("' +
				key +
				'" | "' +
				val +
				'") was stored in localStorage.'
		);
		in_ls.innerHTML = '';
		in_ls.innerHTML = '';
	};

	emptyButton.onclick = function() {
		localStorage.clear();
		alert('info', 'localStorage was emptied.');
	};

	let arr = [];
	for (let i = 0; i < localStorage.length; i++) {
		arr.push(localStorage.key(i));
	}
	for (let i = 0; i < arr.length; i++) {
		out_ls_key.innerHTML += '<li>' + arr[i] + '</li>';
	}

	let list = out_ls_key.getElementsByTagName('li');
	for (let i = 0; i < list.length; i++) {
		list[i].onmouseover = function() {
			let val = localStorage.getItem(this.innerHTML);
			if (val.length > 50000) {
				out_ls_val.value = 'Item-length > 50.000';
				return;
			}
			out_ls_val.value = val;
		};
	}
}
