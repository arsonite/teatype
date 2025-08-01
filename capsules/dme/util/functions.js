function percentage(val1, val2, val3) {
    return (val1 * val2) / val3;
}

function round(decimal) {
    let string = '' + decimal;
    string = string.replace(/^.*\./g, '').substring(0, 1);
    let comata = parseInt(string);
    if (comata >= 5) {
        return Math.round(decimal);
    } else {
        return Math.floor(decimal);
    }
}

function hash(item1, item2, length) {
    let l;
    if (length === undefined) {
        l = 6;
    } else {
        l = length;
    }
    let item = item1 + item2;
    let hash = 0;
    let chr;
    if (item.length === 0) {
        return hash;
    }
    for (let i = 0; i < item.length; i++) {
        chr = item.charCodeAt(i);
        hash = ((hash << 5) - hash) + chr;
        hash |= 0;
    }
    hash = '' + Math.abs(hash);
    hash = hash.substring(0, l);
    return hash;
}

function roll(chance) {
    return Math.random() <= chance;
}

function randomRoll() {
    return Math.random() <= Math.Random();
}

function inflictDamage(dmgPack) {
    let dmgCap = dmgPack[0];
    let baseFluct = dmgCap * 1.0875;
    let min = dmgCap * 0.875;
    let max = baseFluct - min;
    if (roll(dmgPack[1])) {
        return {
            crit: true,
            dmg: Math.floor(dmgPack[2] *= (Math.random() * max + min))
        };
    } else {
        return {
            crit: false,
            dmg: Math.floor(Math.random() * max + min)
        };
    }
}

function calculateDamage(vig, alc) {
    let dmgCap = 1.0;
    let critChance = 0.05;
    let critDmg = 1.0;
    dmgCap += (dmgCap + vig + alc) / 2;
    critChance += (alc / 768);
    critDmg += (vig / 256);
    return [dmgCap, critChance.toFixed(2), critDmg.toFixed(2)];
}
/*if(m.getMentalState() == 2) {
    for(Trait t : trt) {
        // TODO: Wrong Trait-ID, read from file
        //Checks
        if(t.getID() == 3) {
            //
            if(m.getProgress() >= 6 && m.getProgress() < 8) {
                //Distributes the bonus
                dmgCap*= 1.15;
                critChance*= 1.1;
                critDmg*= 1.35;
            } else if (m.getProgress() == 8) {
                dmgCap*= 1.35;
                critChance*= 1.2;
                critDmg*= 1.65;
            }
        }
    }
}*/

function alphaFormula(age, att1, att2, fac1, fac2) {
    let rad = (age + 15 + 45) * (Math.PI / 180);
    let ageFac = 50.0 * (Math.sin(rad));
    let alpha = ageFac + (att1 * fac1) + (att2 * fac2);
    return round(alpha);
}

function betaFormula(trc) {
    return ((6.4 + trc) * trc) - ((3.2 + trc) * trc) + (trc / (trc + 16));
}

function calculateHealth(fit, vig, age) {
    return round(alphaFormula(age, fit, vig, 10, 1.5));
}

function calculateStamina(fit, alc, age) {
    return round(alphaFormula(age, fit, alc, 1.5, 2));
}

function calculateGrant(trc) {
    return round(betaFormula(trc));
}

function calculateXPNeeded(lvl) {
    if(lvl < 1) {
       return;
    }
    return (lvl + 160.5) * Math.pow(2, lvl / 9);
}

function convertLVLtoXP() {

}

function convertXPtoLVL() {

}

function convertCurrencies() {

}

function sacrificeHealth(hlt, trc) {
    return (hlt / 16.0) - (betaFormula(trc) / 8.0);
}

function calculateBloodAmount(sex, hght, wght) {
    if (sex.equals("Male")) {
        return (0.3669 * (Math.pow(hght, 3)) + (0.03219 * wght + 0.6041));
    } else {
        return (0.3561 * (Math.pow(hght, 3)) + (0.03308 * wght + 0.1833));
    }
}

function calculateBMI(hght, wght) {
    return wght / (Math.pow(hght, 2));
}

function randomizeAttributes(lvl) {
    let points = 7;
    let base = 70;
    let min = 1;
    let sum = base + (points * lvl);
    let att = [];

    let rSum = 0;
    for (let i = 0; i < 7; i++) {
        let r = round(Math.random() * sum + min);
        att[i] = r;
        rSum += r;
    }
    let co = sum / rSum;
    rSum = 0;
    for (let i = 0; i < att.length; i++) {
        att[i] = round(att[i] * co);
        rSum += att[i];
    }

    if (rSum > sum) {
        let r = round(Math.random() * 7);
        let diff = rSum - sum;
        att[r] -= diff;
    } else if (rSum < sum) {
        let r = round(Math.random() * 7);
        let diff = sum - rSum;
        att[r] += diff;
    }

    return att;
}

/*
public void random(int lvl) throws Exception {
	Random rnd = new Random();
	int bonusEXP;
	if(lvl > 1 && lvl <= 83) {
		bonusEXP = 7 * lvl;
	} else if (lvl > 83) {
		bonusEXP = (7 * lvl) + (int) (lvl / 90.0 * 100 - 90 + 1);
	} else if (lvl > 85) {
		throw new LevelOutOfBoundsException(lvl);
	} else {
		bonusEXP = 0;
	}
	int m = 101 + bonusEXP;
	int min = 1;
	int max = m - min * 7;
	for(int i = 1; i < att.length; i++) {
		att[i]+= rnd.nextInt(max);
	}
	Arrays.sort(att, 1, att.length);
	for(int i = 1; i < att.length; i++) {
		att[i-1] = att[i] - att[i-1] + min;
	}
	att[att.length-1] = max - att[att.length-1] + min;
	attributesToUtil();
}

function randomizeAttributes(lvl, att) {
    let bonusEXP;
    if (lvl > 1 && lvl <= 83) {
        bonusEXP = 7 * lvl;
    } else if (lvl > 83) {
        bonusEXP = (7 * lvl) + (lvl / 90.0 * 100 - 90 + 1);
    } else if (lvl > 85) {
        throw new Error(lvl);
    } else {
        bonusEXP = 0;
    }
    let m = 101 + bonusEXP;
    let min = 1;
    let max = m - min * 7;
    for (let i = 1; i < att.length; i++) {
        att[i] += Math.random()*max;
    }
    Arrays.sort(att, 1, att.length);
    for (let i = 1; i < att.length; i++) {
        att[i - 1] = att[i] - att[i - 1] + min;
    }
    att[att.length - 1] = max - att[att.length - 1] + min;
}
*/
