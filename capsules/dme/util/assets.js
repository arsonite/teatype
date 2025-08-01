/* Permanent Database JSON-Parsed Objects */
const ATTRIBUTES = null;
const CHARACTER = null;
const FOCUS = {
    'PATHS': {
        'Vatrakumo': parse(focusURL, 'vatrakumo'),
        'Raftel': parse(focusURL, 'raftel')
    }
};

const MIND = {
    'MORALITY': parse(mindURL, 'morality'),
    'MENTALITY': parse(mindURL, 'mentality'),
    'POLITICS': parse(mindURL, 'politics'),
    'ABSOLUTE_JUSTICE': parse(mindURL, 'absolute_justice'),
    'PRIME_EVIL': parse(mindURL, 'prime_evil')
};

const TRAIT = {
    'AQUIRABLE': parse(traitURL, 'aquirable'),
    'PICKABLE': parse(traitURL, 'pickable')
};

console.log(FOCUS);
console.log(MIND);
console.log(TRAIT);

/* Core-Assets */
const Asset = require(coreAssetsURL + 'Asset.js');
const Attributes = require(coreAssetsURL + 'Attributes.js');
const Body = require(coreAssetsURL + 'Body.js');
const Focus = require(coreAssetsURL + 'Focus.js');
const Inventory = require(coreAssetsURL + 'Inventory.js');
const Mind = require(coreAssetsURL + 'Mind.js');
const Skills = require(coreAssetsURL + 'Skills.js');
const Status = require(coreAssetsURL + 'Status.js');
const Traits = require(coreAssetsURL + 'Traits.js');

/* Extended Assets */
const Character = require(coreAssetsURL + 'Character.js');
const NPC = require(assetsURL + 'NPC.js');
const Player = require(assetsURL + 'Player.js');
