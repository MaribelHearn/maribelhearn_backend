const parse06 = require("./parse06")

/**
 * A wrapper for th13 and th14 parsers
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse06or06nc(replay) {
    let version = replay.readUInt16LE(4);
    switch (version) {
        case 0x0102:    // original
            return parse06(replay);
        case 0x010B:    // new classic
            throw new Error("EoSD New Classic has not been implemented, please wait warmly.");
    }

    // rip replay
    throw new Error("Cannot determine th06 version.")
}

module.exports = parse06or06nc