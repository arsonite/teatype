let webFrame = require('electron').webFrame;
webFrame.setZoomFactor(1);
webFrame.setVisualZoomLevelLimits(1, 1);
webFrame.setLayoutZoomLevelLimits(0, 0);

/* RGB-To-Hex */
function componentToHex(c) {
    let hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function RGBtoHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

/* Hex-To-RGB */
function hexToRGB(hex) {
    let shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, (m, r, g, b) => {
        return r + r + g + g + b + b;
    });

    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

/* Filter functions */
function invertColor(hex) {
    if (hex.indexOf('#') === 0) {
        hex = hex.slice(1);
    }
    if (hex.length === 3) {
        hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
    }
    var r = (255 - parseInt(hex.slice(0, 2), 16)).toString(16),
        g = (255 - parseInt(hex.slice(2, 4), 16)).toString(16),
        b = (255 - parseInt(hex.slice(4, 6), 16)).toString(16);
    return '#' + padZero(r) + padZero(g) + padZero(b);
}

function padZero(str, len) {
    len = len || 2;
    var zeros = new Array(len).join('0');
    return (zeros + str).slice(-len);
}

function smartFontColor(color) {
    let temp = hexToRGB(color);
    temp = (temp.r + temp.g + temp.b) / 3;
    if(temp > 128) {
        temp = '#000';
    } else {
        temp = '#FFF';
    }
    return temp;
}

function brightenHex(hex, factor) {
    let rgb = hexToRGB(hex);
    rgb.b += factor;
    rgb.g += factor;
    rgb.r += factor;
    rgb = RGBtoHex(rgb);
    return rgb;
}

function darkenHex(hex, factor) {}

function brightenRGB(rgb, factor) {}

function darkenRGB(rgb, factor) {}
