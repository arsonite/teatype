class Focus extends Asset {
    constructor(path, type, id, name, desc, levels) {
        super(name, desc);
        this.id = id;
        
        this.path = path;
        this.type = type;
        this.levels = levels;
    }

    compile() {
        let desc = this.desc;
        let levels = this.levels;
        let stats = [];
        let amount = 0;
        
        for (let i = 1; i < levels.length; i++) {
            for (let i2 = 1; i2 < levels[i].length; i2++) {
                amount = levels[i].length;
                stats[i2] += '/' + levels[i][i2];
            }
        }

        for (let i = 1; i < amount; i++) {
            stats[i] = stats[i].replace('undefined/', '');
            desc = desc.replace('-' + i + '-', stats[i]);
        }

        let s = '' +
            this.path + ' (' + this.type + ')' + n2 +
            
            this.name + n +
            '(' + this.id + ')' + n2 +

            desc;

        return s;
    }

    getStat(p, n) {
        return this.levels[p, n];
    }
}

module.exports = Focus;
