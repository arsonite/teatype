module.exports = class Module {
	constructor(
		nav,
		name,
		abbr,
		parent = undefined,
		path = undefined,
		bgPath = undefined
	) {
		this.nav = nav;
		this.name = name;
		this.abbr = abbr;
		if (path !== undefined) {
			this.imgW = path + abbr + '_white.png';
			this.imgO = path + abbr + '_orange.png';
		}
		if (bgPath !== undefined) {
			this.bgImg = bgPath + abbr + '.png';
		}
		this.parent === undefined ? (this.parent = parent) : '';
	}

	getNav() {
		return this.nav;
	}

	getAbbrevation() {
		return this.abbr;
	}

	getName() {
		return this.name;
	}

	getImages() {
		return [this.imgW, this.imgO];
	}

	getBackgroundImage() {
		return this.bgImg;
	}

	getParent() {
		return this.parent;
	}

	getHeader() {
		let p1 = p({ id: 'p1', innerHTML: this.getParent() });
		let p2 = p({ id: 'p2', innerHTML: this.getName() });
		return [p1, p2];
	}

	getContent() {}
};
