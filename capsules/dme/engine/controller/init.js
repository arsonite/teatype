let foci = new Array(1);
let traits = new Array(1);
let skills = new Array(1);

/*
let foci = new Array(1);
parseFoci();
console.log(foci);

let traits = new Array(1);
parseTraits();
console.log(traits);

function parseTraits() {
    xml = readFile(absoluteURL + 'res/db/stats/traits/', 'pickable.xml');
    xml = parseXML(xml);

    let xmlTraits = getNodes('trait', xml);

    for (let x of xmlTraits) {
        let xID = x.getAttribute('id');
        let xName = getValue(x, 'name');
        let xDesc = getValue(x, 'desc').trim();
        let xQuote = getValue(x, 'quote').replace(/\"/g, '');

        let xLevels = new Array(1);
        let xLvls = x.getElementsByTagName('lvl');
        for (let l of xLvls) {
            let xNs = l.getElementsByTagName('stat');
            let xN = new Array(1);
            for (let n of xNs) {
                xN.push(n.childNodes[0].nodeValue);
            }

            xLevels.push(xN);
        }

        traits.push(new Trait(
            xID,
            xName,
            xDesc,
            xQuote,
            xLevels
        ));
    }
}

function parseFoci() {
    xml = readFile(absoluteURL + 'res/db/stats/focus/', 'vatrakumo.xml');
    xml = parseXML(xml);

    let xmlFoci = getNode('foci', xml);
    let xPath = getNode('path', xml);
    let xPathName = xPath.getAttribute('name');
    let xType = getValue(xPath, 'type');

    let xmlTraits = getNodes('focus', xml);

    for (let x of xmlTraits) {
        let xID = x.getAttribute('id');
        let xName = getValue(x, 'name');
        let xDesc = getValue(x, 'desc').trim();

        let xLevels = new Array(1);
        let xLvls = x.getElementsByTagName('lvl');
        for (let l of xLvls) {
            let xNs = l.getElementsByTagName('stat');
            let xN = new Array(1);
            for (let n of xNs) {
                xN.push(n.childNodes[0].nodeValue);
            }

            xLevels.push(xN);
        }

        foci.push(new Focus(
            xPathName,
            xType,
            xID,
            xName,
            xDesc,
            xLevels
        ));
    }
}
*/
