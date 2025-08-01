class Character {
    constructor() {
        this.name = '';
        this.sex = '';
        this.race = '';
        this.bday = '';
        this.bplace = '';
        this.age = 0;
        this.app = [];
        this.fact = '';
        this.occup = '';
        this.resid = '';
        this.reli = '';
        this.pol = [];
        this.moral = new Array(12);
        this.createArrays(this.moral);

        this.psycho = [];
        this.philo = [];
        this.rels = new Array(3);
        this.createArrays(this.rels);

        this.mood = '';
        this.desc = '';
        this.bio = '';

        this.creation = this.pullDate();
        this.changed = 'clean';
    }

    setName(name) {
        this.name = name;
        this.flag();
    }

    createArrays(arr) {
        for (let i = 0; i < arr.length; i++) {
            arr[i] = [];
        }
    }

    flag() {
        this.changed = this.pullDate();
    }

    pullDate() {
        let date = new Date();
        let d = date.getDay + '.' + date.getMonth + '.' + date.getFullYear;
        let h = date.getHours + ':' + date.getMinutes + ':' + date.getSeconds + ':' + date.getMilliseconds;

        return d + ' ' + h;
    }

    getPattern(trim) {
        let n = '\n';
        let t = '\t';
        let pattern = [
          '[Name]',
            'Sex',
            'Race',
            'Age',
            'Birthdate',
            'Birthplace',
            'Appearance [List]',
            'Faction',
            'Occupation',
            'Residence',
            'Religion',
            'Political Views [List]',
            'Moral Compass [12]',
            '   Honesty',
            '   Humanism',
            '   Kindness',
            '   Forgiveness',
            '   Inherent Rights',
            '   Theft',
            '   Adultery',
            '   Violence',
            '   Murder',
            '   Drugs',
            '   Law',
            '   War',
            'Psychology [List]',
            'Philosophy [List]',
            'Relations [3]',
            '   Affection [List]',
            '   Neutral [List]',
            '   Distain [List]',
            'Mood',
            'Description',
            'Biography'];
        if (trim) {
            for(let i = 0; i < pattern.length; i++) {
                pattern[i] = pattern[i].replace(/\[.*\]/g, '');
                pattern[i] = pattern[i].replace(/\s+/g, '');
            }
        }
        return pattern;
    }

    printPattern(trim) {
        let pattern = this.getPattern(trim);
        let s = '';

        for (var x of pattern) {
            s += x + '\n';
        }
        return s.trim();
    }

    iCloudFormat() {

    }

    toString() {
        let n = '\n';
        let s = '';

        return s;
    }
};

module.exports = Character;