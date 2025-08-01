function create(element) {
    return document.createElement(element);
}

function insertBefore(target, element) {
    target.insertAdjacentElement('beforebegin', element);
}

function insertAfter(target, element) {
    target.insertAdjacentElement('afterend', element);
}

function insertBeforeHTML(target, html) {
    target.insertAdjacentElement('beforebegin', html);
}

function insertAfterHTML(target, html) {
    target.insertAdjacentElement('afterend', html);
}

function id(id) {
    return document.getElementById(id)
}

function c(c, target) {
    if (target === undefined) {
        return document.getElementsByClassName(c)[0];
    }
    return target.getElementsByClassName(c)[0];
}

function classes(c, target) {
    if (target === undefined) {
        return document.getElementsByClassName(c);
    }
    return target.getElementsByClassName(c);
}

function tag(tag, target) {
    if (target === undefined) {
        return document.getElementsByTagName(tag)[0];
    }
    return target.getElementsByTagName(tag)[0];
}

function tags(tag, target)  {
    if (target === undefined) {
        return document.getElementsByTagName(tag);
    }
    return target.getElementsByTagName(tag);
}
