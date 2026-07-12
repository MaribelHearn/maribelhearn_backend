const KaitaiStream = require("kaitai-struct/KaitaiStream")
const { decrypt06, unlzss } = require("thrpy-decode")
const Th07 = require("../ksy/Th07")
const C = require("../constants")
const dayjs = require("dayjs")
    .extend(require("dayjs/plugin/customParseFormat"))

/**
 * Parses th07 replay and returns the replay's information
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse07(replay) {
    let compData = replay.subarray(16)
    compData = decrypt06(compData, replay.at(13))
    const compDataSize = replay.readUInt32LE(20)

    const decrypted = Buffer.concat([replay.subarray(0, 16), compData.subarray(0, 68), unlzss(compData.subarray(68, 68 + compDataSize))])

    // Replay
    const R = new Th07(new KaitaiStream(decrypted))

    // Base info
    const info = {
        game: C.GAME.TH07.ID,
        shot: R.header.shot,
        difficulty: R.header.difficulty,
        score: R.header.score * 10,
        // Only day and month are included
        date: dayjs(R.header.date, "MM/DD").toDate(),
        name: R.header.name.replace(/\0/g, ""),
        slowdown: R.header.slowdown
    }

    // Get info for each stage
    const stages = []
    R.stages.forEach((stage, i, S) => {
        if (R.fileHeader.stageOffsets[i] === 0)
            return

        stages.push({
            stage: i,
            score: (stages.length === 0) ? 0 : S[stages.at(-1).stage].body.score * 10,
            point_items: stage.body.pointItems,
            graze: stage.body.graze,
            piv: stage.body.piv,
            power: stage.body.power,
            lives: stage.body.lives,
            bombs: stage.body.bombs,
            cherry: stage.body.cherry,
            cherry_max: stage.body.cherryMax
        })
    })
    info["stages"] = stages

    // Type of replay
    info["type"] = (
        stages.filter(stages => stages !== null).length === 1 && 
        (R.header.difficulty !== C.DIFFICULTY.EXTRA && R.header.difficulty !== C.DIFFICULTY.PHANTASM)
    ) ? C.REPLAY_TYPE.STAGE_PRACTICE : C.REPLAY_TYPE.FULL_GAME
    
    return info
}

module.exports = parse07