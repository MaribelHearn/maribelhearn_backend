const KaitaiStream = require("kaitai-struct/KaitaiStream")
const { decrypt, unlzss } = require("thrpy-decode")
const Th128 = require("../ksy/Th128")
const ThModern = require("../ksy/ThModern")
const C = require("../constants")
const dayjs = require("dayjs")

/**
 * Parses th128 replay and returns the replay's information
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse128(replay) {
    const header = new ThModern(new KaitaiStream(replay))
    let compData = Buffer.from(header.main.compData)
    compData = decrypt(compData, 0x800, 0x5E, 0xE7)
    compData = decrypt(compData, 0x80, 0x7D, 0x36)

    // Replay
    const R = new Th128(new KaitaiStream(unlzss(compData)))

    // Base info
    const info = {
        game: C.GAME.TH128.ID,
        shot: "Cirno",
        difficulty: R.header.difficulty,
        route: R.header.route,
        score: R.header.score * 10,
        // TODO: Will check if the date is shown properly
        date: dayjs.unix(R.header.timestamp).toDate(),
        name: R.header.name.replace(/\0/g, ""),
        slowdown: R.header.slowdown
    }

    // Get info for each stage
    const stages = []
    R.stages.forEach((stage) => {
        stages.push({
            stage: stage.stageNum - 1,
            score: stage.score * 10,
            graze: stage.graze,
            motivation: stage.motivation,
            perfect_freeze: stage.perfectFreeze,
            frozen_area: stage.frozenArea
        })
    })
    info["stages"] = stages

    // Type of replay
    // In case somebody decides to upload a thprac stage practice replay
    info["type"] = (
        stages.filter(stages => stages !== null).length === 1 && 
        R.header.difficulty !== C.DIFFICULTY.EXTRA
    ) ? C.REPLAY_TYPE.STAGE_PRACTICE : C.REPLAY_TYPE.FULL_GAME
    
    return info
}

module.exports = parse128