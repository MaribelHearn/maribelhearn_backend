const fs = require("fs/promises");
const path = require("path");
const { parse } = require("./thrpy-parser");
const TABLE = {
	th06: {
		title: "EoSD",
		shot: ["ReimuA", "ReimuB", "MarisaA", "MarisaB"]
	},
	th07: {
		title: "PCB",
		shot: ["ReimuA", "ReimuB", "MarisaA", "MarisaB", "SakuyaA", "SakuyaB"]
	},
	th08: {
		title: "IN",
		shot: [
			"Border Team",
			"Magic Team",
			"Scarlet Team",
			"Ghost Team",
			"Solo Reimu",
			"Solo Yukari",
			"Solo Marisa",
			"Solo Alice",
			"Solo Sakuya",
			"Solo Remilia",
			"Solo Youmu",
			"Solo Yuyuko"
		],
		stage: ["1", "2", "3", "4A", "4B", "5", "6A", "6B", "Ex"]
	},
	th09: {
		title: "PoFV",
		shot: [
			"Reimu",
			"Marisa",
			"Sakuya",
			"Youmu",
			"Reisen",
			"Cirno",
			"Lyrica",
			"Mystia",
			"Tewi",
			"Yuuka",
			"Aya",
			"Medicine",
			"Komachi",
			"Eiki",
			"Merlin",
			"Lunasa"
		],
		stage: ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
	},
	th10: {
		title: "MoF",
		shot: ["Reimu", "Marisa"],
		subshot: ["A", "B", "C"]
	},
	th11: {
		title: "SA",
		shot: ["Reimu", "Marisa"],
		subshot: ["A", "B", "C"]
	},
	th12: {
		title: "UFO",
		shot: ["Reimu", "Marisa", "Sanae"],
		subshot: ["A", "B"]
	},
	th128: {
		title: "GFW",
		shot: ["Cirno"],
		route: ["A1", "A2", "B1", "B2", "C1", "C2", "Ex"],
		stage: [
			"A1-1",
			"A1-2",
			"A1-3",
			"A2-2",
			"A2-3",
			"B1-1",
			"B1-2",
			"B1-3",
			"B2-2",
			"B2-3",
			"C1-1",
			"C1-2",
			"C1-3",
			"C2-2",
			"C2-3",
			"Ex"
		]
	},
	th13: {
		title: "TD",
		shot: ["Reimu", "Marisa", "Sanae", "Youmu"]
	},
	th14: {
		title: "DDC",
		shot: ["Reimu", "Marisa", "Sakuya"],
		subshot: ["A", "B"]
	},
	th15: {
		title: "LoLK",
		shot: ["Reimu", "Marisa", "Sanae", "Reisen"]
	},
	th16: {
		title: "HSiFS",
		shot: ["Reimu", "Cirno", "Aya", "Marisa"],
		season: ["Spring", "Summer", "Autumn", "Winter"]
	},
	th17: {
		title: "WBaWC",
		shot: ["Reimu", "Marisa", "Youmu"],
		subshot: ["Wolf", "Otter", "Eagle"]
	},
	th18: {
		title: "UM",
		shot: ["Reimu", "Marisa", "Sakuya", "Sanae"]
	},
	difficulty: ["Easy", "Normal", "Hard", "Lunatic", "Extra", "Phantasm"],
	type: ["Full game", "Stage practice", "Spell practice", "Versus"],
	stage: ["1", "2", "3", "4", "5", "6", "Ex"]
}

async function parseReplay(file) {
	const buffer = await fs.readFile(file);
	try {
		const result = parse(buffer);

		// Filter file
		// if (result.type != 0)
		// 	throw "Not a full run";

		let shot = TABLE[result.game].shot[result.shot];
		if (TABLE[result.game].subshot)
			shot += TABLE[result.game].subshot[result.subshot];
		else if (TABLE[result.game].season)
			shot += TABLE[result.game].season[result.season];

		let final = (result.stages?.find((stage) => stage.stage == 7) != undefined) ? "B" : "A";

		// const row = [
		// 	path.basename(path.dirname(file)),
		// 	path.basename(file),
		// 	result.game,
		// 	TABLE.type[result.type],
		// 	TABLE.difficulty[result.difficulty],
		// 	shot,
		// 	(result.game == "th08") ? final : "",
		// 	result.score,
		// 	result.date.toISOString(),
		// 	`"${result.name}"`,
		// ]
		const row = result.score;

		return {
			success: true,
			row: row
		};
	} catch (err) {
		return {
			success: false,
			row: [
				path.basename(path.dirname(file)),
				path.basename(file),
				err
			]
		}
	}
}

async function parseDir(dir) {
	const files = await fs.readdir(dir);
	console.log(`Found ${files.length} replays from ${dir}`);

	const results = await Promise.all(files.map(file => parseReplay(`${dir}/${file}`)));
	return results;
}

const SOURCE_DIR = process.argv[2] ?? "replays";
const CSV_OUTPUT = process.argv[3] ?? "processed.csv";
const CSV_ERR = process.argv[4] ?? "unprocessed.csv";

// fs.readdir(SOURCE_DIR).then(async (dirs) => {
// 	console.log("Parsing in progress, please wait warmly...");
// 	const results_nested = await Promise.all(dirs.map(dir => parseDir(`${SOURCE_DIR}/${dir}`)));
// 	const results = [].concat(...results_nested);
// 	const dataRows = results.filter(result => result.success && result.row.length > 0).map(result => result.row.join(","));
// 	const errorRows = results.filter(result => !result.success).map(result => result.row.join(","));

// 	// Write to CSV
// 	const dataHeader = "Source,Replay,Game,Type,Difficulty,Shot,Final,Score,Date,Player";
// 	await fs.writeFile(CSV_OUTPUT, dataHeader + '\n' + dataRows.join("\n"));

// 	const errorHeader = "Source,Replay,Reason";
// 	await fs.writeFile(CSV_ERR, errorHeader + '\n' + errorRows.join("\n"));

// 	console.log("Done");
// }).catch(err => {
// 	console.error(err);
// });

parseReplay(process.argv[2]).then(data => {
	console.log(data.row)
}).catch(err => {
	console.error(err);
})
