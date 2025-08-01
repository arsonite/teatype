module.exports = class Person {
    constructor() {
        this.names = [];
        this.surname = '';
        this.sex = '';
    }

    setNames(name) {
        this.names.push(name);
    }

    setSurname(surname) {
        this.surname = surname;
    }

    setSex(sex) {
        this.sex = sex;
    }

    getNames() {
        let name = '';
        for(var n of this.names) {
            name += n + ' '
        }
        return name;
    }

    getSurname() {
        return this.surname;
    }
    
    getFullName() {
        let fullName = '';
        fullName = this.getNames() + this.getSurname();
        return fullName;
    }

    getSex() {
        return this.sex;
    }
};
