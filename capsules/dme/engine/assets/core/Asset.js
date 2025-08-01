class Asset {
    constructor(name, desc) {
        if (!arguments.length) {
            this.name = this.desc = '';
        } else {
            this.name = name;
            this.desc = desc;
        }
    }
}

module.exports = Asset;