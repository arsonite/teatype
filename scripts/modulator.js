/* Persistent HTML-Elements */
let head,
	body,
	nav,
	nav_point,
	nav_sub,
	main,
	main_header,
	main_content,
	alerts,
	footer,
	refresher,
	btn_dom,
	btn_log;

let bg, hex_bg;

// Modules array instead of objects, anonymous init in loader
const modules = {
	/* Home */
	nav_home: new NavigationHome('home', '', 'home', 'home', navURL, logoURL),
	home_cssvars: new CSSVariables('home', 'css-variables', 'cssvars', 'home'),
	home_encrypt: new Encryption('home', 'encryption', 'encrypt', 'home'),
	home_kgen: new KGenerator('home', 'k-generator', 'kgen', 'home'),
	home_passgen: new PasswordGenerator(
		'home',
		'password-generator',
		'passgen',
		'home'
	),
	home_namealloc: new RandomNameAllocator(
		'home',
		'random name allocator',
		'namealloc',
		'home'
	),
	home_namegen: new RandomNameGenerator(
		'home',
		'random name generator',
		'namegen',
		'home'
	),
	home_regex: new Regex('home', 'regular expression', 'regex', 'home'),
	home_rgbhex: new RGBToHEX('home', 'rgb to hex', 'rgbhex', 'home'),
	home_speaker: new Speaker('home', 'speaker', 'speaker', 'home'),

	/* The Human Alien */
	nav_tha: new NavigationTHA(
		'tha',
		'',
		'tha',
		'the human alien',
		navURL,
		logoURL
	),
	tha_gali: new RGBToHEX('tha', 'galaxy-index', 'gali', 'the human alien'),
	tha_starSysGen: new RGBToHEX(
		'tha',
		'star system generator',
		'starSysGen',
		'the human alien'
	),

	/* The Schlong of Zen */
	nav_tsz: new NavigationTSZ(
		'tsz',
		'',
		'tsz',
		'the schlong of zen',
		navURL,
		logoURL
	),
	tsz_anomscal: new AnomalyScale(
		'tsz',
		'anomaly-scale',
		'anomscal',
		'the schlong of zen'
	),
	tsz_rels: new Relations('tsz', 'relations', 'rels', 'the schlong of zen'),

	/* The Wicked Saga */
	nav_tws: new NavigationTWS(
		'tws',
		'',
		'tws',
		'the wicked saga',
		navURL,
		logoURL
	),
	tws_maps: new Maps('tws', 'maps', 'maps', 'the schlong of zen'),

	/* Dead Men's End */
	nav_dme: new NavigationDME(
		'dme',
		'',
		'dme',
		"dead men's end",
		navURL,
		logoURL
	),
	dme_maps: new Debug('dme', 'debug', 'debug', "dead men's end"),
	dme_docs: new Documentation('dme', 'documentation', 'docs', "dead men's end"),
	dme_launcher: new Launcher('dme', 'launcher', 'launcher', "dead men's end")
};

let currentPage = 'nav_home';

function resetMain() {
	main_header.innerHTML = main_content.innerHTML = '';
}

// TODO: Rewrite functionality into navigateable 2d array (like in TempoEX Reloaded)
function resetNavPoints() {
	for (let i = 0; i < nav_point.length; i++) {
		nav_point[i].style.color = '#DDD';
	}
	resetNavSubs();

	let navImgs = nav.getElementsByTagName('img');
	for (let i = 0; i < navImgs.length; i++) {
		if (navImgs[i].src.includes('orange')) {
			navImgs[i].className = 'hidden';
		} else {
			navImgs[i].className = '';
		}
	}
}

function resetNavSubs() {
	for (let i = 0; i < nav_sub.length; i++) {
		nav_sub[i].style.color = '#353535';
	}
}

function changeCurrentPoint(point) {
	resetNavPoints();

	let tempPoint = id(point);
	tempPoint.style.color = '#FF8800';
	swapImages(tempPoint);
}

function changeSelectedSub(sub) {
	resetNavPoints();

	let e1 = id(sub);
	let e2 = e1.parentNode;
	let e3 = e2.parentNode;

	e1.style.color = '#FFF';
	e3.getElementsByTagName('a')[0].style.color = '#FF8800';
	swapImages(e3);
}

function swapImages(element) {
	element.getElementsByTagName('img')[0].className = 'hidden';
	element.getElementsByTagName('img')[1].className = '';

	if (element.className.includes('nav')) {
		hex_bg.className = ' hidden';

		let bgImg = document.createElement('img');
		bgImg.src = modules[element.id].getBackgroundImage();
		bgImg.className = 'bg_img';
		bgImg.height = NAV_BG_SIZE;
		bgImg.width = NAV_BG_SIZE;

		let imgs = bg.getElementsByClassName('bg_img');

		if (imgs.length > 0) {
			bg.replaceChild(bgImg, bg.getElementsByClassName('bg_img')[0]);
		} else {
			bg.appendChild(bgImg);
		}
		return;
	}
	hex_bg.className = '';

	removeByClass('bg_img', bg);
}

/**
 * Function to navigate to clicked navigation stubs.
 *
 * @param {*} key
 */
function navigate(key) {
	new Audio(sfxURL + 'soft_wish.wav').play();

	currentPage = key;

	resetMain();

	if (key.includes('nav')) {
		changeCurrentPoint(key);
	} else {
		changeSelectedSub(key);
	}

	main_header.appendChild(modules[key].getHeader()[0]);
	main_header.appendChild(modules[key].getHeader()[1]);
	main_content.appendChild(modules[key].getContent());

	sendDOM();
}

document.addEventListener('DOMContentLoaded', () => {
	/* Parse the mandatory elements */
	head = tag('head');
	body = tag('body');

	nav = tag('nav');
	main = tag('main');
	alerts = id('alerts');

	bg = id('bg');
	hex_bg = id('hex_bg');
	teatype_logo = id('teatype_logo');
	home_logo = id('home_logo');
	tha_logo = id('tha_logo');
	tsz_logo = id('tsz_logo');
	tws_logo = id('tws_logo');
	dme_logo = id('dme_logo');

	footer = tag('footer');
	refresher = id('refresher');
	btn_dom = id('btn_dom');
	btn_log = id('btn_log');

	/* Dynamically altering main contents */
	main_header = id('main_header');
	main_content = id('main_content');

	/* Creating dynamically allocated navigation points and stubs */
	for (let module in modules) {
		let m = modules[module];

		if (module.includes('nav')) {
			let dropdown = div({ className: 'dropdown' });

			let dropdownList = div({ className: 'dropdown-list' });

			let navPoint = document.createElement('a');
			navPoint.id = module;
			navPoint.className = 'nav_point';
			navPoint.text = m.getAbbrevation();

			let imgW = document.createElement('img');
			imgW.src = m.getImages()[0];
			imgW.height = NAV_IMG_SIZE;
			imgW.width = NAV_IMG_SIZE;

			let imgO = document.createElement('img');
			imgO.src = m.getImages()[1];
			imgO.height = NAV_IMG_SIZE;
			imgO.width = NAV_IMG_SIZE;

			navPoint.appendChild(imgW);
			navPoint.appendChild(imgO);
			dropdown.appendChild(navPoint);
			dropdown.appendChild(dropdownList);
			nav.appendChild(dropdown);
			continue;
		}

		let navSub = document.createElement('a');
		navSub.id = m.getNav() + '_' + m.getAbbrevation();
		navSub.className = 'nav_sub';
		navSub.text = m.getName();

		let dropdown = document.getElementById('nav_' + m.getNav()).parentNode;
		dropdown = className('dropdown-list', dropdown);

		dropdown.appendChild(navSub);
	}

	nav_point = classNames('nav_point');
	nav_sub = classNames('nav_sub');

	/* Misc onClick-Events */
	btn_dom.onclick = () => {
		if (domWindowCreated) {
			domWindow.close();
		}
		createDomWindow();
	};

	btn_log.onclick = () => {
		if (logWindowCreated) {
			logWindow.close();
		}
		createLogWindow();
	};

	/* Append sound effects and objects to nav */
	for (let i = 0; i < nav_point.length; i++) {
		nav_point[i].onclick = () => {
			navigate(nav_point[i].id);
		};

		nav_point[i].onmouseenter = () => {
			smallClick();
		};
	}

	for (let i = 0; i < nav_sub.length; i++) {
		nav_sub[i].onclick = () => {
			navigate(nav_sub[i].id);
		};

		nav_sub[i].onmouseenter = () => {
			softClick();
		};
	}

	footer.onclick = () => {
		// Not for footer but for little arrow right up that expands blur menu
		//new Audio(sfxURL + 'woosh.wav').play();
		//new Audio(sfxURL + 'splashy_click.wav').play();
	};

	navigate(currentPage);
});
