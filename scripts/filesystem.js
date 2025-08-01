const fs = require('fs');

/* Custom node FileSystem-API */
function createFile(path, file, ext) {
	fs.writeFile(path + file + '.' + ext, '', 'utf8', function(err) {
		if (err) throw err;
	});
}

function writeFile(path, file, ext, content) {
	fs.writeFile(path + file + '.' + ext, content, 'utf8', function(err) {
		if (err) throw err;
	});
}

function readFile(path, file, ext) {
	return fs.readFileSync(path + file + '.' + ext, 'utf8');
}

function readDirectory(path) {
	return fs.readdirSync(path);
}
