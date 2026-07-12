const KaitaiStream = require("kaitai-struct/KaitaiStream")
const { decrypt06, unlzss } = require("thrpy-decode")
const Th08 = require("../ksy/Th08")
const Th08Userdata = require("../ksy/Th08Userdata")
const C = require("../constants")
const dayjs = require("dayjs")

/**
 * Parses th08 replay and returns the replay's information
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse08(replay) {
    const compDataSize = replay.readUInt32LE(12) - 24
    let compData = replay.subarray(24, compDataSize)
    compData = decrypt06(compData, replay.at(21))

    const decrypted = Buffer.concat([replay.subarray(0, 24), compData.subarray(0, 80), unlzss(compData.subarray(80))])

    // Replay
    const R = new Th08(new KaitaiStream(decrypted))
    // Userdata
    const U = new Th08Userdata(new KaitaiStream(replay))

    // Base info
    const info = {
        game: C.GAME.TH08.ID,
        shot: R.header.shot,
        difficulty: R.header.difficulty,
        score: R.header.score * 10,
        date: dayjs(U.userdata.date.value).toDate(),
        name: R.header.name.replace(/\0/g, ""),
        slowdown: R.header.slowdown
    }

    // Spell practice
    if (R.header.spellCardId !== C.NO_SPELL_CARD_ID) {
        info["type"] = C.REPLAY_TYPE.SPELL_PRACTICE
        info["spell_card_id"] = R.header.spellCardId

        return info
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
            time: stage.body.time,
            piv: stage.body.piv,
            power: stage.body.power,
            lives: stage.body.lives,
            bombs: stage.body.bombs,
        })

        // Final A or B
        if (i === 6)
            info["final"] = "A"
        if (i === 7)
            info["final"] = "B"
    })
    info["stages"] = stages

    // Type of replay
    info["type"] = (
        stages.filter(stages => stages !== null).length === 1 && 
        R.header.difficulty !== C.DIFFICULTY.EXTRA
    ) ? C.REPLAY_TYPE.STAGE_PRACTICE : C.REPLAY_TYPE.FULL_GAME
    
    return info
}

module.exports = parse08