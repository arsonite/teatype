class NPC extends Character {
    constructor(name, desc, id, age, sex, origin, title, perculiar) {
        super(name, desc, age, sex, origin, title, perculiar);
        
        this.slainXP = 0;

        this.id = '#N';
        if (id !== '') {
            this.id += id;
        }
        this.flag = 'NPC';

        this.profession = '';
        this.align = {
            'Alignment': '',
            'Score': 0
        };
        
        this.assignPronouns();

        this.crucial = false;

        this.index = parseInt(id.replace('#N', ''));
        npcs[this.index] = this;
    }

    assignPronouns() {
        if (this.sex === 'Male') {
            this.pn = pnM;
            this.PN = PNM;
        } else {
            this.pn = pnF;
            this.PN = PNF;
        }
    }
}

module.exports = NPC;