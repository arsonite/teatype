/* Requires */
const $ = require('jquery');
const fs = require('fs');

/* Absolute URLs */
const absoluteURL = '/Users/burak/Desktop/Projekte/Coding/Web-Entwicklung/Electron/TeaType Collection/src/window_modules/dme/';

const resURL = absoluteURL + 'res/';

const imgURL = resURL + 'img/';
const iconURL = imgURL + 'icon/';
const armor = imgURL + 'armor/';
const bodyURL = imgURL + 'body/';

const dbURL = resURL + 'db/';
const preURL = dbURL + 'pre/';
const focusURL = preURL + 'focus/';
const mindURL = preURL + 'mind/';
const traitURL = preURL + 'traits/';

const assetsURL = absoluteURL + 'engine/assets/';
const coreAssetsURL = assetsURL + 'core/';

/* CSS Constants */
const ANIM_DURATION_HEALTH = 1.5;
const ANIM_DURATION_STAMINA = 1;
const ANIM_DURATION_GRANT = 2;

/* Pronouns */
const pnFPS = ['i', 'me', 'my'];
const pnM = ['he', 'him', 'his'];
const pnF = ['she', 'her', 'hers'];
const pnI = ['it', 'its', 'its'];

const PNFPS = ['I', 'Me', 'My'];
const PNM = ['He', 'Him', 'His'];
const PNF = ['She', 'Her', 'Hers'];
const PNI = ['It', 'Its', 'Its'];

/* Constant Values */
const EXP_MAX = 128256512;
const ARM_MAX = 1048;
const LVL_CAP = 700;

const MORAL_RANGE = [-250, 250];
const MORAL_MAX_SUM = MORAL_RANGE[1] * 2;

/* String Symbols */
const n = '\n';
const n2 = n + n;
const n3 = n + n2;

const t = '\t';
const t2 = t + t;
const t3 = t + t2;

const tm = '> ';
