const fs = require("fs/promises");
const path = require("path");
const { exit } = require("process");
const { parse } = require("./thrpy-parser");

async function parseReplay(file) {
	const buffer = await fs.readFile(file);
	const result = parse(buffer);
	return result.score;
}

parseReplay(process.argv[2]).then(score => {
	console.log(score);
	exit(0);
}).catch(err => {
	console.error(err);
	exit(1);
});
