function tsz_db_HTML() {
	main_header.innerHTML =
		n2 +
		'<p id="p1">The Schlong of Zen </p>' +
		n2 +
		'<p id="p2">Database</p>' +
		n1;
}

function tsz_db_functions() {
	let Character = require('../../js/tsz/character.js');

	lg.setScriptName('db.js');

	////////// HTML-Nodes //////////

	let form_anomaly = document.createElement('form');
	form_anomaly.id = 'form_anomaly';

	let form_character = document.createElement('form');
	form_character.id = 'form_character';

	let form_faction = document.createElement('form');
	form_faction.id = 'form_faction';

	let form_location = document.createElement('form');
	form_location.id = 'form_location';

	let in_textarea = document.createElement('textarea');
	in_textarea.placeholder = 'Enter Data';
	in_textarea.class = 'textarea_write';
	in_textarea.rows = '30';

	let out_pattern = document.createElement('textarea');
	out_pattern.id = 'out_pattern';
	out_pattern.readOnly = true;

	let store = document.createElement('button');
	store.type = 'button';
	store.id = 'store';
	store.innerHTML = 'Store';

	const grey = '#BBB';
	const white = '#EEE';

	document.addEventListener('DOMContentLoaded', function(event) {
		let p_anomaly = $('#p_anomaly')[0];
		let p_character = $('#p_character')[0];
		let p_faction = $('#p_faction')[0];
		let p_location = $('#p_location')[0];

		let left_container = $('#left_container')[0];
		let right_container = $('#right_container')[0];

		let storeBtn = $('#store')[0];

		let boolAnomaly, boolCharacter, boolFaction, boolLocation;

		p_anomaly.onclick = showAnomaly;
		p_character.onclick = showCharacter;
		p_faction.onclick = showFaction;
		p_location.onclick = showLocation;

		showAnomaly();

		function showAnomaly() {
			boolAnomaly = true;
			boolCharacter = false;
			boolFaction = false;
			boolLocation = false;

			p_anomaly.style.color = white;
			p_character.style.color = grey;
			p_faction.style.color = grey;
			p_location.style.color = grey;

			refreshMain();

			left_container.appendChild(form_anomaly);
			form_anomaly.appendChild(in_textarea);
		}

		function showCharacter() {
			boolAnomaly = false;
			boolCharacter = true;
			boolFaction = false;
			boolLocation = false;

			p_anomaly.style.color = grey;
			p_character.style.color = white;
			p_faction.style.color = grey;
			p_location.style.color = grey;

			refreshMain();

			left_container.appendChild(form_character);
			form_character.appendChild(in_textarea);

			out_pattern.rows = '34';
			out_pattern.cols = '7';
			out_pattern.value = new Character().printPattern(false);
			right_container.appendChild(out_pattern);
			right_container.appendChild(store);
		}

		function showFaction() {
			boolAnomaly = false;
			boolCharacter = false;
			boolFaction = true;
			boolLocation = false;

			p_anomaly.style.color = grey;
			p_character.style.color = grey;
			p_faction.style.color = white;
			p_location.style.color = grey;

			refreshMain();

			left_container.appendChild(form_faction);
			form_faction.appendChild(in_textarea);
		}

		function showLocation() {
			boolAnomaly = false;
			boolCharacter = false;
			boolFaction = false;
			boolLocation = true;

			p_anomaly.style.color = grey;
			p_character.style.color = grey;
			p_faction.style.color = grey;
			p_location.style.color = white;

			refreshMain();

			left_container.appendChild(form_location);
			form_location.appendChild(in_textarea);
		}

		function refreshMain() {
			left_container.innerHTML = '';
			right_container.innerHTML = '';
		}

		store.onclick = function() {
			if (boolAnomaly) {
				storeAnomaly();
			} else if (boolCharacter) {
				storeCharacter();
			} else if (boolFaction) {
				storeFaction();
			} else if (boolLocation) {
				storeLocation();
			}
		};

		function storeAnomaly() {}

		function storeCharacter() {
			let val = in_textarea.value;
			let char = new Character();

			let keys = [
				'Name',
				'Age',
				'Sex',
				'Appearance',
				'Faction',
				'Occupation',
				'Residence',
				'Religion',
				'Political Views',
				'Moral Compass',
				'Psychology',
				'Philosophy',
				'Relations',
				'Mood',
				'Description',
				'Biography'
			];
			let moralKeys = [
				'Honesty',
				'Humanism',
				'Kindness',
				'Forgiveness',
				'Inherent Rights',
				'Theft',
				'Adultery',
				'Violence',
				'Murder',
				'Drugs',
				'Law',
				'War'
			];
			let relKeys = ['Affection', 'Neutral', 'Distain'];

			let pattern = char.getPattern(true);

			for (let i = 0; i <= pattern.length; i++) {
				val = val.replace(pattern[i], '');
			}

			val = val.trim();

			let arr = val.split('\n');
			for (let i = 0; i < arr.length; i++) {
				arr[i] = arr[i].trim();
			}

			let filePath = 'res/db/tsz/characters/';
			let fileName = arr[0];
			fileName = fileName.trim();
			fileName = fileName.replace(/\s+/g, '_');
			fileName = fileName.toLowerCase();

			createFile(filePath, fileName);
			writeString(filePath, fileName, character.toString());
		}

		function storeFaction() {}

		function storeLocation() {}
	});
}
