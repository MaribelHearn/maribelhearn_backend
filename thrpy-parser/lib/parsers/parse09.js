const KaitaiStream = require("kaitai-struct/KaitaiStream")
const { decrypt06, unlzss } = require("thrpy-decode")
const Th09 = require("../ksy/Th09")
const C = require("../constants")
const dayjs = require("dayjs")
    .extend(require("dayjs/plugin/customParseFormat"))

/**
 * Parses th09 replay and returns the replay's information
 * @param {Buffer} replay 
 * @returns Information about the replay
 */
function parse09(replay) {
    const compDataSize = replay.readUInt32LE(12) - 24
    let compData = replay.subarray(24, compDataSize)
    compData = decrypt06(compData, replay.at(21))

    const decrypted = Buffer.concat([replay.subarray(0, 24), compData.subarray(0, 168), unlzss(compData.subarray(168))])

    // Replay
    const R = new Th09(new KaitaiStream(decrypted))

    // Base info
    const info = {
        game: C.GAME.TH09.ID,
        difficulty: R.header.difficulty,
        date: dayjs(R.header.date, "YY/MM/DD").toDate(),
        name: R.header.name.replace(/\0/g, "")
    }
    
    if (R.fileHeader.stageOffsets[9] === 0) {
        // Story mode
        info["type"] = C.REPLAY_TYPE.FULL_GAME
        
        // Get info for each stage
        const stages = []

        let finalStage = -1
        for (let i = 0; i < 9; i++) {
            if (R.fileHeader.stageOffsets[i] === 0)
                continue

            finalStage = i

            const p1 = R.stages[i].body
            const p2 = R.stages[i + 10].body

            stages.push({
                stage: i,
                score: p1.score * 10,
                lives: p1.lives,
                p2_shot: p2.shot,
                p2_score: p2.score * 10,
            })
        }
        const p1 = R.stages[finalStage].body
        info["shot"] = p1.shot
        // This is not the final score, the game doesn't store final score into the replay
        info["score"] = p1.score * 10
        info["stages"] = stages
    } else {
        // PVP mode
        // TODO: Complete filling info for PVP replays
        throw new Error("PoFV PVP replays are currently unsupported.")
    }
    
    return info
}

module.exports = parse09