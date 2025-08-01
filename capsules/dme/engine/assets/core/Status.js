class Status extends Asset {
    constructor(name, desc, id) {
        super(name,  desc);
        this.id = id;
    }
}

module.exports = Status;