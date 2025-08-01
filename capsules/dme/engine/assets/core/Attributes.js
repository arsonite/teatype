class Attributes {
    constructor(fit, vig, alc, bri, awe, emp, trc) {
        this.vals = [];
        if (arguments.length == 1) {
            this.vals = randomizeAttributes(arguments[0]);
        } else {
            if ((fit + vig + alc + bri + awe + emp + trc) <= LVL_CAP) {
                for (let att of arguments) {
                    this.vals.push(att);
                }
            }
        }

        this.add();

        this.vals = {
            'Fitness': this.vals[0],
            'Vigor': this.vals[1],
            'Alacrity': this.vals[2],
            'Brilliance': this.vals[3],
            'Awareness': this.vals[4],
            'Empathy': this.vals[5],
            'Transcendence': this.vals[6]
        }
        this.leth = {
            'Lethargy': 0
        }
    }

    add() {
        this.sum = 0;
        for (let i = 0; i < this.vals.length; i++) {
            this.sum += this.vals[i];
        }
    }
}

module.exports = Attributes;

/*
public void levelUp(int exp, int atr) {
	att[atr]+= exp;
	attributesToUtil();
}

public boolean isGodlike() {
	int sum = 0;
	for(int i : att) {
		sum+=i;
	}
	if(sum == LVL_CAP) {
		return true;
	} else {
		return false;
	}
}
*/
