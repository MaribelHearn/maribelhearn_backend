const fs = require("fs/promises");
const path = require("path");
const { exit } = require("process");
const { parse } = require("./thrpy-parser");

async function parseReplay(file) {
	const buffer = await fs.readFile(file);
	const result = parse(buffer);
	return result;
}

parseReplay(process.argv[2]).then(data => {
	console.log(`{"score": ${data.score}, "date": "${data.date.toISOString().split('T')[0]}"}`);
	exit(0);
}).catch(err => {
	console.error(err);
	exit(1);
});
