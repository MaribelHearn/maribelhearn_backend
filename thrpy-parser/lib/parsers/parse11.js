const KaitaiStream = require("kaitai-struct/KaitaiStream")
const { decrypt, unlzss } = require("thrpy-decode")
const Th11 = require("../ksy/Th11")
const ThModern = require("../ksy/ThModern")
const C = require("../constants")
const dayjs = require("dayjs")

/**
 * Parses th11 replay and returns the replay's information
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse11(replay) {
    const header = new ThModern(new KaitaiStream(replay))
    let compData = Buffer.from(header.main.compData)
    compData = decrypt(compData, 0x800, 0xAA, 0xE1)
    compData = decrypt(compData, 0x40, 0x3D, 0x7A)

    // Replay
    const R = new Th11(new KaitaiStream(unlzss(compData)))

    // Base info
    const info = {
        game: C.GAME.TH11.ID,
        shot: R.header.shot,
        subshot: R.header.subshot,
        difficulty: R.header.difficulty,
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
            piv: stage.piv,
            power: stage.power,
            lives: stage.lives,
            life_pieces: stage.lifePieces
        })
    })
    info["stages"] = stages

    // Type of replay
    info["type"] = (
        stages.filter(stages => stages !== null).length === 1 && 
        R.header.difficulty !== C.DIFFICULTY.EXTRA
    ) ? C.REPLAY_TYPE.STAGE_PRACTICE : C.REPLAY_TYPE.FULL_GAME
    
    return info
}

module.exports = parse11