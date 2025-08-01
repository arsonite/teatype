let xml = '';
let parser = new DOMParser();
let serializer = new XMLSerializer();

function getNodes(node, xml) {
    return xml.getElementsByTagName(node);
}

function getNode(node, xml) {
    return xml.getElementsByTagName(node)[0];
}

function getAttribute(att, node, xml) {
    let temp = xml.getElementsByTagName(node)[0];
    return temp.getAttribute(att);
}

function getValue(node, val) {
    return node.getElementsByTagName(val)[0].childNodes[0].nodeValue;
}

function serializeXML(xml) {
    return serializer.serializeToString(xml);
}

function parseXML(xml) {
    return parser.parseFromString(xml, 'text/xml');
}

function showXML(xml) {
    log('', parseXML(xml));
}
