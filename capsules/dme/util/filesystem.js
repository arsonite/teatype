function createFile(path, file, ext) {
    fs.writeFile(path + file + '.' + ext, '', 'utf8', function (err) {
        if (err) throw err;
    });
}

function writeFile(path, file, ext, content) {
    fs.writeFile(path + file + '.' + ext, content, 'utf8', function (err) {
        if (err) throw err;
    });
}

function readFile(path, file, ext) {
    return fs.readFileSync(path + file + '.' + ext, 'utf8');
}

function appendString(path, file, ext, content, lineBreak) {
    let s = content;
    if (lineBreak) {
        s = '\n' + content;
    }
    fs.appendFile(path + file + '.' + ext, s, function (err) {
        if (err) throw err;
    });
}

function parse(path, file) {
    return JSON.parse(readFile(path, file, 'json'));
}