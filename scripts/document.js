/* Creation methods */
function create(element, config = _) {
	let el = document.createElement(element);

	if (config !== _) {
		config.id !== _ ? (el.id = config.id) : '';
		config.className !== _ ? (el.className = config.className) : '';
		config.value !== _ ? (el.value = config.value) : '';
		config.innerHTML !== _ ? (el.innerHTML = config.innerHTML) : '';
		config.onclick !== _ ? (el.onclick = config.onclick) : '';
	}

	return el;
}

function div(config) {
	let div = create('div', config);
	return div;
}

function span(config) {
	let span = create('span', config);
	return span;
}

function p(config) {
	let p = create('p', config);
	return p;
}

function form(config) {
	let form = create('form', config);
	return form;
}

function input(id = _, className = _, type = _, placeholder = _, label = _) {
	let inputBox = create('div');
	inputBox.className = 'input';

	let input = create('input');

	id !== _ ? (input.id = id) : _;
	className !== _ ? (input.className = className) : _;
	type !== _ ? (input.type = type) : _;
	placeholder !== _ ? (input.placeholder = placeholder) : _;

	if (label !== _) {
		let span = create('span');
		span.className = 'label';
		span.innerHTML = label;
		inputBox.appendChild(span);
	}
	inputBox.appendChild(input);

	inputBox.setInput = value => {
		input.value = value;
	};

	inputBox.input = () => {
		return input.value;
	};
	return inputBox;
}

function radio(id = _, className = _, name = _, text, checked = false) {
	let label = create('label');
	label.className = 'radio';

	let input = create('input');
	id !== _ ? (input.id = id) : _;
	className !== _ ? (input.className = className) : _;
	name !== _ ? (input.name = name) : _;
	input.checked = checked;
	input.type = 'radio';
	label.appendChild(input);

	let span = create('span');
	label.appendChild(span);

	let p = create('p');
	p.innerHTML = text;
	label.appendChild(p);

	label.checked = () => {
		return input.checked;
	};

	return label;
}

function check(id = _, className = _, text, checked = false) {
	let label = create('label');
	label.className = 'checkbox';

	let input = create('input');
	id !== _ ? (input.id = id) : _;
	className !== _ ? (input.className = className) : _;
	input.checked = checked;
	input.type = 'checkbox';
	label.appendChild(input);

	let span = create('span');
	label.appendChild(span);

	let p = create('p');
	p.innerHTML = text;
	label.appendChild(p);

	label.checked = () => {
		return input.checked;
	};

	return label;
}

/* Insertion methods */
function insertBefore(target, element) {
	target.insertAdjacentElement('beforebegin', element);
}

function insertAfter(target, element) {
	target.insertAdjacentElement('afterend', element);
}

function insertBeforeHTML(target, html) {
	target.insertAdjacentElement('beforebegin', html);
}

function insertAfterHTML(target, html) {
	target.insertAdjacentElement('afterend', html);
}

/* Find methods */
function id(id, target = undefined) {
	if (target === undefined) {
		return document.getElementById(id);
	}
	return target.getElementById(id);
}

function classNames(c, target = undefined) {
	if (target === undefined) return document.getElementsByClassName(c);
	return target.getElementsByClassName(c);
}

function className(c, target = undefined) {
	if (target === undefined) {
		return classNames(c, document)[0];
	}
	return classNames(c, target)[0];
}

function tags(tag, target = undefined) {
	if (target === undefined) return document.getElementsByTagName(tag);
	return target.getElementsByTagName(tag);
}

function tag(tag, target = undefined) {
	if (target === undefined) return tags(tag, document)[0];
	return tags(tag, target)[0];
}

/* Removal methods */
function removeByClass(className, target = undefined) {
	var elements = (target === undefined
		? document
		: target
	).getElementsByClassName(className);

	while (elements.length > 0) {
		elements[0].parentNode.removeChild(elements[0]);
	}
}

/**
 * A short function to simply copy an object instead of referencing it
 *
 * @param {Object} object
 */
function clone(object) {
	return JSON.parse(JSON.stringify(obj));
}

/**
 * A short function to simply copy an element instead of referencing it
 *
 * @param {Object} element
 * @param {Boolean} cloneChildNodes
 */
function clone(element, cloneChildNodes) {
	return element.cloneNode(cloneChildNodes);
}
