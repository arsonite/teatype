/* Absolute URLs */
const remote = require('electron').remote.app;

const slash = remote.getAppPath().includes('\\') ? '\\' : '/';

const absoluteURL = remote.getAppPath() + slash;
const dbURL = `${absoluteURL}db${slash}`;

const moduleURL = `${absoluteURL}modules${slash}`;
const homeURL = `${moduleURL}home${slash}`;

const scriptURL = `${absoluteURL}scripts${slash}`;

const resURL = `${absoluteURL}res${slash}`;
const sfxURL = `${resURL}sfx${slash}`;
const musicURL = `${resURL}music${slash}`;

const imgURL = `${resURL}img${slash}`;
const navURL = `${imgURL}nav${slash}`;
const iconURL = `${imgURL}icon${slash}`;
const logoURL = `${imgURL}logo${slash}`;

/* Constant values */
const NAV_IMG_SIZE = 13; // TODO: CSS is better
const NAV_BG_SIZE = 250; // TODO: CSS is better

/* Utility-Classes */
const Loader = require(scriptURL + 'loader.js');
const Logger = require(scriptURL + 'logger.js');
const Module = require(scriptURL + 'module.js');
const _ = undefined;

/* Unicode-Operations */
const n = '\n';
const t = '\t';

const t2 = t + t;
const t3 = t + t2;
const t4 = t + t3;
const t5 = t + t4;

const n1 = n + t;
const n2 = n + t2;
const n3 = n + t3;
const n4 = n + t4;

/* Modulator modules */
const NavigationHome = require(homeURL + '_nav.js');
const CSSVariables = require(homeURL + 'cssVariables.js');
const Encryption = require(homeURL + 'encryption.js');
const KGenerator = require(homeURL + 'kGenerator.js');
const PasswordGenerator = require(homeURL + 'passwordGenerator.js');
const RandomNameAllocator = require(homeURL + 'randomNameAllocator.js');
const RandomNameGenerator = require(homeURL + 'randomNameGenerator.js');
const Regex = require(homeURL + 'regex.js');
const RGBToHEX = require(homeURL + 'rgbToHex.js');
const Speaker = require(homeURL + 'speaker.js');

const NavigationTHA = require(moduleURL + '/tha/_nav.js');
const GalaxyIndex = require(moduleURL + '/tha/galaxyIndex.js');
const StarSystemGenerator = require(moduleURL + '/tha/starSystemGenerator.js');

const NavigationTSZ = require(moduleURL + '/tsz/_nav.js');
const AnomalyScale = require(moduleURL + '/tsz/anomalyScale.js');
const Relations = require(moduleURL + '/tsz/relations.js');

const NavigationTWS = require(moduleURL + '/tws/_nav.js');
const Maps = require(moduleURL + '/tws/maps.js');

const NavigationDME = require(moduleURL + '/dme/_nav.js');
const Debug = require(moduleURL + 'dme/debug.js');
const Documentation = require(moduleURL + 'dme/docs.js');
const Launcher = require(moduleURL + 'dme/launcher.js');

/* Site-wide utilities */
const names = new Loader('datasets/names/');
