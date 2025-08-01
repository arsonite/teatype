class Player extends Character {
    constructor(name, desc, age, sex, origin, title, att) {
        super(name, desc, age, sex, origin, title, true, att);
        this.id = '#P000000';

        this.flag = 'Player';

        this.rep = {
            'Reputation': '',
            'Score': 0
        };

        this.pn = pnFPS;
        this.PN = PNFPS;

        this.mind = new Mind();
        this.skls = new Skills();
        this.stat = new Status();
        this.trts = new Traits();
    }
    
    /* Player has to visit an exchanger or bank to convert his currencies */
    convertCurrencies() {}

    setMoralityScores(murder, theft, rape, violence, adultery, vigilance, dishonesty, resent, irrationality) {
        this.mind.setMoralityScores(murder, theft, rape, violence, adultery, vigilance, dishonesty, resent, irrationality);
    }

    updateGUI_stats_window() {}

    updateGUI_bars() {
        let perc = '%';
        let percH = percentage(this.hlt, 100, this.maxHlt);
        let percS = percentage(this.stm, 100, this.maxStm);
        let percG = percentage(this.grn, 100, this.maxGrn);

        health_bar.style.width = percH + perc;
        stamina_bar.style.width = percS + perc;
        grant_bar.style.width = percG + perc;

        let p1 = tag('p', health_bar);
        let p2 = tag('p', stamina_bar);
        let p3 = tag('p', grant_bar);

        p1.innerHTML = this.hlt;
        p2.innerHTML = this.stm;
        p3.innerHTML = this.grn;

        /* TODO: Needs to be revisited, until which percent when <45 doesnt apply anymore? */
        let calculateSlow = function (dur, perc) {
            if (perc === 0) {
                return 0;
            }
            let tan100 = 45;
            let tan = function (deg) {
                return Math.tan(deg * (Math.PI / 180));
            }
            let slowFactor = 15;

            let slow = function (perc) {
                let temp = 1 - (perc / 100);
                temp = 1 + temp;
                temp = tan100 * temp - slowFactor;
                if (temp < 45) {
                    temp = 45;
                }
                return temp;
            }
            let tanTemp = slow(perc);
            tanTemp = dur * tan(tanTemp);
            return tanTemp;
        }

        let sec = 's';
        let durH = calculateSlow(ANIM_DURATION_HEALTH, percH) + sec;
        let durS = calculateSlow(ANIM_DURATION_STAMINA, percS) + sec;
        let durG = calculateSlow(ANIM_DURATION_GRANT, percG) + sec;

        let anim_H = id('health_img', health);
        anim_H = tag('img', anim_H);
        anim_H.style.animationDuration = durH;

        let anim_S = id('stamina_img', stamina);
        anim_S = tag('img', anim_S);
        anim_S.style.animationDuration = durS;

        let anim_G = id('grant_img', grant);
        anim_G = tag('img', anim_G);
        anim_G.style.animationDuration = durG;
    }

    updateGUI_mind_grid() {
        let mind = this.mind.moral;
        let sum = {
            'r': 0,
            'g': 0,
            'b': 0
        };

        let i = 0;
        Object.keys(mind).forEach(key => {
            let score = mind[key].score;
            let span = tag('span', m[i]);

            let color;
            if (score === MORAL_RANGE[0]) {
                color = MIND.PRIME_EVIL.BG;
                span.style.color = MIND.PRIME_EVIL.font;
            } else if (score === MORAL_RANGE[1]) {
                color = MIND.ABSOLUTE_JUSTICE.BG
                span.style.color = MIND.ABSOLUTE_JUSTICE.font;
            } else {
                color = MORAL_RANGE[1] + score;
                color = percentage(color, 100, MORAL_MAX_SUM);
                color = Math.floor(percentage(255, color, 100));
                color = RGBtoHex(color, color, color);
                span.style.color = smartFontColor(color);
            }

            let rgb = hexToRGB(color);
            sum.r += rgb.r;
            sum.g += rgb.g;
            sum.b += rgb.b;

            /* TODO: Insert hr left and right of score */
            span.innerHTML = `<b>${key}</b><br>(${score})<br>${mind[key].desc}`;
            span.style.backgroundColor = color;
            m[i].style.backgroundColor = color;
            i++;
        });
        sum.r = Math.floor(sum.r / (i + 1));
        sum.g = Math.floor(sum.g / (i + 1));
        sum.b = Math.floor(sum.b / (i + 1));
        sum = RGBtoHex(sum.r, sum.g, sum.b);

        let div = tag('div', mind_box);
        let span = tag('span', div);
        span.style.backgroundColor = sum;
        span.innerHTML = `My mind is <b>${this.mind.mentalState}</b>, because I feel <b>${this.mind.mentalProg}</b><br>(${this.mind.sum})`;
        mind_box.onmouseenter = () => {
            span.style.visibility = 'visible';
            span.style.opacity = '1';
        }

        mind_box.onmouseleave = () => {
            span.style.visibility = 'hidden';
            span.style.opacity = '0';
        }

        mind_box.style.backgroundColor = sum;
    }

    updateGUI_profile() {
        let s = '';

        s = `<p id="p_lvl">LVL: <b>${this.lvl}</b><p><br>` +
            `<p id="p_copper">Copper: <b>${this.copper}</b><p>` +
            `<p id="p_silver">Silver: <b>${this.silver}</b><p>` +
            `<p id="p_gold">Gold: <b>${this.gold}</b><p><br>` +
            `Age: <b>${this.age}</b><br>` +
            `Days: <b>${this.age * 365}</b>`;

        profile.innerHTML = s;
    }

    updateGUI_attributes() {
        Object.keys(this.att.vals).forEach(key => {
            let li1 = create('li');
            let li2 = create('li');
            let k = `${key}`;
            let v = `<b>${this.att.vals[key]}</b>`;

            let div = create('div');
            let span = create('span');

            li1.innerHTML = k;
            li2.innerHTML = v;
            attributes1.appendChild(li1);
            attributes2.appendChild(li2);
        });
    }

    updateGUI_XP() {
        let span = tag('span', exp_frame);
        span.innerHTML = '256 / 512';
        exp_bar.style.width = '50%';
    }
}

module.exports = Player;
