class RandomNameAllocator extends Module {
	constructor(nav, name, abbr, parent) {
		super(nav, name, abbr, parent, _, _);
	}

	getContent() {
		let root = div({ id: 'namealloc' });
		let box = div({ className: 'box' });
		root.appendChild(box);

		/* ContentBox #1 */
		let selectors = div({ id: 'selectors', className: 'container' });
		box.appendChild(selectors);

		let dynamic = div({ id: 'dynamic', className: 'container' });
		box.appendChild(dynamic);

		let template = div({ id: 'template', className: 'container' });
		box.appendChild(template);

		/* ContentBox #2 */
		let hr = create('hr');
		box = div({ id: 'hr', className: 'box' });
		box.appendChild(hr);
		root.appendChild(box);

		/* ContentBox #3 */
		let ul = create('ul');
		box = div({ className: 'box' });
		box.appendChild(ul);
		root.appendChild(box);

		return root;
	}
}

module.exports = RandomNameAllocator;

/*
class RandomNameAllocator extends Module {
	constructor(nav, name, abbr, parent) {
		super(nav, name, abbr, parent, _, _);

		this.index = 2;
		this.tables = [];
		this.selectors = [];
	}

	getContent() {
		let root = div({ id: 'namealloc' });
		let box = div({ className: 'box' });
		root.appendChild(box);

		let selectors = div({ id: 'selectors', className: 'container' });
		box.appendChild(selectors);

		let dynamic = div({ id: 'dynamic', className: 'container' });
		box.appendChild(dynamic);

		let template = div({ id: 'template', className: 'container' });
		box.appendChild(template);

		let selectDataSet = element => {
			let index =
				typeof element == 'number' ? element : parseInt(element.target.id);
			this.index = index;

			for (let i = 0; i < this.selectors.length; i++) {
				this.selectors[i].className = this.selectors[i].className.replace(
					/selected/g,
					''
				);
				this.tables[i].className = this.tables[i].className.replace(
					/hidden/g,
					''
				);
				this.tables[i].className += ' hidden';
			}

			this.selectors[index].className += ' selected';
			this.tables[index].className = this.tables[index].className.replace(
				/hidden/g,
				''
			);
		};

		const RACIAL_KEYS = ['black', 'white', 'hispanic', 'indian', 'random'];
		const arr = names.getAll();
		for (let i = 0; i < Object.keys(arr).length; i++) {
			let table = div(Object.keys(arr)[i], 'table hidden');

			dynamic.appendChild(table);
			this.tables.push(table);

			let tableSelector = p(i, 'selector', Object.keys(arr)[i], selectDataSet);
			selectors.appendChild(tableSelector);

			this.selectors.push(selectors.childNodes[i]);

			let genderGroup = form('genderGroup', _);
			let genderLabel = span(_, 'label', 'Gender');
			genderGroup.appendChild(genderLabel);

			let radioMale = radio('male', _, genderGroup.id, 'Only male names', true);
			genderGroup.appendChild(radioMale);

			let radioFemale = radio('female', _, genderGroup.id, 'Only female names');
			genderGroup.appendChild(radioFemale);

			let radioBoth = radio('both', _, genderGroup.id, 'Both names');
			genderGroup.appendChild(radioBoth);

			let racialFirstnamesGroup = form();
			let racialFirstnamesLabel = span(_, 'label', 'Racial firstnames');
			racialFirstnamesGroup.appendChild(racialFirstnamesLabel);

			let racialSurnamesGroup = form();
			let racialSurnamesLabel = span(_, 'label', 'Racial surnames');
			racialSurnamesGroup.appendChild(racialSurnamesLabel);

			let dataset = names.getAll()[table.id];
			Object.keys(dataset).forEach(key => {
				if (key === 'firstnames') {
					if (dataset['firstnames']['male'] !== undefined) {
						table.appendChild(genderGroup);
					}

					if (!Array.isArray(dataset['firstnames']['male'])) {
						table.appendChild(racialFirstnamesGroup);
						RACIAL_KEYS.forEach(racialKey => {
							if (dataset['firstnames']['male'][racialKey] !== undefined) {
								racialFirstnamesGroup.appendChild(
									check(racialKey, _, racialKey)
								);
							}
						});
					}
				} else if (key === 'surnames') {
					if (!Array.isArray(dataset['surnames'])) {
						table.appendChild(racialSurnamesGroup);
						RACIAL_KEYS.forEach(racialKey => {
							if (dataset[key][racialKey] !== undefined) {
								racialSurnamesGroup.appendChild(check(racialKey, _, racialKey));
							}
						});
					}
				}
			});
		}
		selectDataSet(this.index);

		let amountInput = input(_, _, 'text', 'n = 100', 'Amount of names');
		amountInput.setInput(100);
		template.appendChild(amountInput);

		let lengthInput = input(_, _, 'text', 'l = 1', 'Amount of firstnames');
		lengthInput.setInput(1);
		template.appendChild(lengthInput);

		let gen = create('button');
		gen.innerHTML = 'Randomly allocate';
		gen.onclick = () => {
			ul.innerHTML = '';

			let n = parseInt(amountInput.input());
			let l = parseInt(lengthInput.input());

			const table = this.tables[this.index];
			const dataset = names.getAll()[table.id];

			let gender = null;
			let genderGroup = tag('form', table);
			genderGroup.childNodes.forEach(label => {
				if (label.className === 'radio') {
					let radio = tag('input', label);
					if (radio.checked) {
						gender = radio.id;
					}
				}
			});

			let racialFirstnames = [];
			let racialFirstnamesGroup = tags('form', table)[1];
			racialFirstnamesGroup !== undefined
				? racialFirstnamesGroup.childNodes.forEach(label => {
						if (label.className === 'checkbox') {
							let checkbox = tag('input', label);
							if (checkbox.checked) {
								racialFirstnames.push(checkbox.id);
							}
						}
				  })
				: '';

			let racialSurnames = [];
			let racialSurnamesGroup = tags('form', table)[2];
			racialSurnamesGroup !== undefined
				? racialSurnamesGroup.childNodes.forEach(label => {
						if (label.className === 'checkbox') {
							let checkbox = tag('input', label);
							if (checkbox.checked) {
								racialSurnames.push(checkbox.id);
							}
						}
				  })
				: '';

			const racialized = racialFirstnames.length > 0;
			const genderized = gender !== 'both';
			const male = genderized ? gender === 'male' : 0;
			let firstnames;
			let surnames = dataset['surnames'];
			if (male) {
				firstnames = dataset['firstnames']['male'];
			} else if (!male) {
				firstnames = dataset['firstnames']['female'];
			} else {
				firstnames = dataset['firstnames']['male'].concat(
					dataset['firstnames']['female']
				);
			}

			for (let i = 0; i < n; i++) {
				let out = '';

				let race;
				if (racialized) {
					let index = Math.floor(Math.random() * racialFirstnames.length);
					race = racialFirstnames[index];

					let r = Math.floor(Math.random() * firstnames[race].length);
					out = firstnames[race][r];
					race = racialFirstnames.length !== 1 ? race : '';
				} else {
					let r = Math.floor(Math.random() * firstnames.length);
					out = firstnames[r];
				}
				out = out.toLowerCase();
				out = out.substr(0, 1).toUpperCase() + out.substr(1, out.length);

				let sur = '';
				if (racialized) {
					let index = Math.floor(Math.random() * racialSurnames.length);
					let r = Math.floor(
						Math.random() * surnames[racialSurnames[index]].length
					);
					sur = surnames[racialSurnames[index]][r];
				} else {
					let r = Math.floor(Math.random() * surnames.length);
					sur = surnames[r];
				}
				sur = sur.toLowerCase();
				sur = sur.substr(0, 1).toUpperCase() + sur.substr(1, sur.length);
				out += ' ' + sur;

				let li = create('li');
				li.innerHTML = out;
				if (racialized) {
					let span = create('span');
					span.className = race;
					span.innerHTML = race.substr(0, 1).toUpperCase();
					li.appendChild(span);
				}
				li.className = genderized ? '' : male ? 'male' : 'female';
				ul.appendChild(li);
			}
		};
		template.appendChild(gen);

		let hr = create('hr');
		box = div('hr', 'box');
		box.appendChild(hr);
		root.appendChild(box);

		let ul = create('ul');
		box = div(_, 'box');
		box.appendChild(ul);
		root.appendChild(box);

		return root;
	}
}

module.exports = RandomNameAllocator;
*/
