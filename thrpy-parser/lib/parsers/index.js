const C = require("../constants")

/**
 * A list of parsers for supported Touhou games
 */

const PARSERS = {}
const parse06 = PARSERS[C.GAME.TH06.MAGIC] = require("./parse06")
const parse07 = PARSERS[C.GAME.TH07.MAGIC] = require("./parse07")
const parse08 = PARSERS[C.GAME.TH08.MAGIC] = require("./parse08")
const parse09 = PARSERS[C.GAME.TH09.MAGIC] = require("./parse09")
const parse10 = PARSERS[C.GAME.TH10.MAGIC] = require("./parse10")
const parse11 = PARSERS[C.GAME.TH11.MAGIC] = require("./parse11")
const parse12 = PARSERS[C.GAME.TH12.MAGIC] = require("./parse12")
const parse128 = PARSERS[C.GAME.TH128.MAGIC] = require("./parse128")
const parse13 = require("./parse13")
const parse14 = require("./parse14")
/**
 * ZUN was drunk and did not change the gamecode for TH14, so this is now used for two games
 * and thus we have to do fuckery to find which one it is
 * fun fact: the games themselves don't test this so if you rename the file you can crash them
 * - raviddog
 */
const parse13or14 = PARSERS[C.GAME.TH13.MAGIC] = require("./parse13or14")
const parse15 = PARSERS[C.GAME.TH15.MAGIC] = require("./parse15")
const parse16 = PARSERS[C.GAME.TH16.MAGIC] = require("./parse16")
const parse17 = PARSERS[C.GAME.TH17.MAGIC] = require("./parse17")
const parse18 = PARSERS[C.GAME.TH18.MAGIC] = require("./parse18")

/**
 * Parse a Touhou replay file. Supported games are
 * th06, th07, th08, th09, th10, th11, th12, th128, th13, th14, th15, th16, th17, th18
 * @param {*} replay 
 */
function parse(replay) {
    // Get the magic number
    const magic = replay.subarray(0, 4)

    // If the magic number matches, pick that parser and parse the replay
    if (String.fromCharCode(...magic) in PARSERS)
        return PARSERS[magic](replay)

    // Otherwise, this replay is either unsupported or not a replay file
    throw new Error("Unsupported replay.")
}

module.exports = {
    parse,
    parse06,
    parse07,
    parse08,
    parse09,
    parse10,
    parse11,
    parse12,
    parse128,
    parse13,
    parse14,
    parse13or14,
    parse15,
    parse16,
    parse17,
    parse18,
}