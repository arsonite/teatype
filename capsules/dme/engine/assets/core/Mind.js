class Mind {
    constructor() {
        this.moral = {};
        Object.keys(MIND.MORALITY).forEach(key => {
            this.moral[key] = {
                'score': 0,
                'desc': ''
            }
        });
        this.sum = 0;
        this.mentalState = '';
        this.mentalProg = '';
    }

    updateMentalState() {
        let ms, mp;
        let sum = this.sum;
        let moral_range0 = MORAL_RANGE[0] * 9;
        let moral_range1 = MORAL_RANGE[1] * 9;
        let moral_max_sum = MORAL_MAX_SUM * 9;

        let index = moral_range1 + sum;
        index = Math.floor(index / (moral_max_sum / 8));

        let key;
        if (sum === moral_range0) {
            key = Object.keys(MIND.PRIME_EVIL.Mentality)[0];
            ms = key;
            mp = MIND.PRIME_EVIL.Mentality[key][1];
        } else if (sum === moral_range1) {
            key = Object.keys(MIND.ABSOLUTE_JUSTICE.Mentality)[0];
            ms = key;
            mp = MIND.ABSOLUTE_JUSTICE.Mentality[key][1];
        } else if (index < 3) {
            key = Object.keys(MIND.MENTALITY)[0];
        } else if (index > 3 && index < 6) {
            index -= 3;
            key = Object.keys(MIND.MENTALITY)[1];
        } else {
            index -= 6;
            key = Object.keys(MIND.MENTALITY)[2];
        }
        ms = key;
        mp = MIND.MENTALITY[key][index];

        this.mentalState = ms;
        this.mentalProg = mp;
    }

    add() {
        this.sum = 0;
        Object.keys(this.moral).forEach(key => {
            this.sum += this.moral[key].score;
        });
    }

    moralityScore(key, score) {
        if (score === undefined) {
            return this.moral[key].score;
        }
        this.moral[key].score = score;
    }

    moralityDescription(key, desc) {
        if (desc === undefined) {
            return this.moral[key].desc;
        }
        this.moral[key].desc = desc;
    }

    setMoralityScores(murder, theft, rape, violence, adultery, vigilance, dishonesty, resent, irrationality) {
        let i = 0;
        Object.keys(this.moral).forEach(key => {
            // TO-DO: Validation of range -250 250 for single items and addition (sum)
            this.moral[key].score = arguments[i];

            if (arguments[i] === MORAL_RANGE[0]) {
                this.moral[key].desc = MIND.PRIME_EVIL.Morality[key];
            } else if (arguments[i] === MORAL_RANGE[1]) {
                this.moral[key].desc = MIND.ABSOLUTE_JUSTICE.Morality[key];
            } else {
                let index = MORAL_RANGE[1] + arguments[i];
                index = Math.floor(index / (MORAL_MAX_SUM / 8));
                this.moral[key].desc = MIND.MORALITY[key][index];
            }
            i++;
        });
        this.add();
        this.updateMentalState();
    }

    setRandom() {}
}

module.exports = Mind;
