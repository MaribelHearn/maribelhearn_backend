const KaitaiStream = require("kaitai-struct/KaitaiStream")
const { decrypt, unlzss } = require("thrpy-decode")
const Th12 = require("../ksy/Th12")
const ThModern = require("../ksy/ThModern")
const C = require("../constants")
const { convertToRealPIV } = require("../utils")
const dayjs = require("dayjs")

/**
 * Parses th12 replay and returns the replay's information
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse12(replay) {
    const header = new ThModern(new KaitaiStream(replay))
    let compData = Buffer.from(header.main.compData)
    compData = decrypt(compData, 0x800, 0x5E, 0xE1)
    compData = decrypt(compData, 0x40, 0x7D, 0x3A)

    // Replay
    const R = new Th12(new KaitaiStream(unlzss(compData)))

    // Base info
    const info = {
        game: C.GAME.TH12.ID,
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
        const stageInfo = {
            stage: stage.stageNum - 1,
            score: stage.score * 10,
            graze: stage.graze,
            piv: convertToRealPIV(info.game, stage.piv),
            power: stage.power,
            lives: stage.lives,
            life_pieces: stage.lifePieces,
            bombs: stage.bombs,
            bomb_pieces: stage.bombPieces
        }

        /**
         * This is the reason when you collect the first life piece of a life
         * it looks like you got 2/5 parts of a life instead of 1/5 for subsequent life pieces
         * It was not an illusion, it was ZUN's shenanigan
         */
        if (stageInfo.life_pieces > 0)
            stageInfo.life_pieces -= 1

        stages.push(stageInfo)
    })
    info["stages"] = stages

    // Type of replay
    info["type"] = (
        stages.filter(stages => stages !== null).length === 1 && 
        R.header.difficulty !== C.DIFFICULTY.EXTRA
    ) ? C.REPLAY_TYPE.STAGE_PRACTICE : C.REPLAY_TYPE.FULL_GAME
    
    return info
}

module.exports = parse12