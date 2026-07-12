const KaitaiStream = require("kaitai-struct/KaitaiStream")
const { decrypt, unlzss } = require("thrpy-decode")
const Th18 = require("../ksy/Th18")
const ThModern = require("../ksy/ThModern")
const C = require("../constants")
const { convertToRealPIV } = require("../utils")
const dayjs = require("dayjs")

/**
 * Parses th18 replay and returns the replay's information
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse18(replay) {
    const header = new ThModern(new KaitaiStream(replay))
    let compData = Buffer.from(header.main.compData)
    compData = decrypt(compData, 0x400, 0x5C, 0xE1)
    compData = decrypt(compData, 0x100, 0x7D, 0x3A)

    // Replay
    const R = new Th18(new KaitaiStream(unlzss(compData)))
    
    // Base info
    const info = {
        game: C.GAME.TH18.ID,
        shot: R.header.shot,
        difficulty: R.header.difficulty,
        score: R.header.score * 10,
        // TODO: Will check if the date is shown properly
        date: dayjs.unix(R.header.timestamp).toDate(),
        name: R.header.name.replace(/\0/g, ""),
        slowdown: R.header.slowdown
    }

    // Spell practice
    if (R.header.spellPracticeId !== C.NO_SPELL_PRACTICE_ID) {
        info["type"] = C.REPLAY_TYPE.SPELL_PRACTICE
        info["spell_card_id"] = R.header.spellPracticeId

        return info
    }

    // Get info for each stage
    const stages = []
    R.stages.forEach((stage) => {
        stages.push({
            stage: stage.stageNum - 1,
            score: stage.stageDataStart.score * 10,
            graze: stage.stageDataStart.graze,
            piv: convertToRealPIV(info.game, stage.stageDataStart.piv),
            power: stage.stageDataStart.power,
            lives: stage.stageDataStart.lives,
            life_pieces: stage.stageDataStart.lifePieces,
            bombs: stage.stageDataStart.bombs,
            bomb_pieces: stage.stageDataStart.bombPieces,
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

module.exports = parse18