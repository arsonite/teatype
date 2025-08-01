const Character = require('character.js');

class Anomaly extends Character {
    constructor(name, surname, age, faction, role, clas, skill, premaw, mood, desc, str, vig, agl, power) {
        super(name, surname, age, faction, role);
        this.clas = clas;
        this.skills = skill;
        this.premaw = premaw;
        this.mood = mood;
        this.desc = desc;
        this.scale = new Array(4);
        this.rating = 0;
        init();
    }

    init() {
        scale[0] = str;
        scale[1] = vig;
        scale[2] = agl;
        scale[3] = power;

        for (let i in scale) {
            rating += i;
        }
    }
};

module.exports = Anomaly;