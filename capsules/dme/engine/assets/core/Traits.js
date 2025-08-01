class Traits {
    constructor() {
        this.points = 0;
        this.aqui = null;
        this.pick = null;
    }

    gainTrait(key) {}

    addTrait(key) {
        let trait = TRAIT.PICKABLE[key];
        let desc = this.parseDescription(trait);
        let stage;

        trait.Description = desc;

        this.pick[key] = trait;
    }

    removeTrait(key) {}

    /* This function parses the ascendancy of the Trait and
     * replaces the placeholders in the description with
     * the corresponding values
     */
    parseDescription(trt) {
        let trait = trt;
        let desc = trait.Description;
        let asc = trait.Ascendancy;
        let concat = [];

        for (let i = 0; i < asc.length; i++) {
            let numbers = false;
            for (let i2 = 0; i2 < asc[i].length; i2++) {
                if (Number.isInteger(asc[i][i2])) {
                    numbers = true;
                }
                concat[i] += asc[i][i2] + '/';
            }
            concat[i] = concat[i].substr(0, concat[i].length - 1);
            if (numbers) {
                concat[i] += '%';
            }
            desc = desc.replace(`-${i+1}-`, concat[i]);
            desc = desc.replace(/undefined/, '');
        }
        return desc;
    }
}

module.exports = Traits;
