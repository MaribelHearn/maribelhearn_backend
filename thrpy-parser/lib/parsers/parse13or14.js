const KaitaiStream = require("kaitai-struct/KaitaiStream")
const ThModern = require("../ksy/ThModern")
const parse13 = require("./parse13")
const parse14 = require("./parse14")

/**
 * A wrapper for th13 and th14 parsers
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse13or14(replay) {
    const header = new ThModern(new KaitaiStream(replay))

    // SJIS character for 廟
    if ([0x90, 0xC9].includes(header.userdata.userDesc[4]))
        return parse13(replay)

    // SJIS character for 城
    if ([0x8B, 0xBB].includes(header.userdata.userDesc[4]))
        return parse14(replay)

    // rip replay
    throw new Error("Cannot determine th13 or th14 replay.")
}

module.exports = parse13or14