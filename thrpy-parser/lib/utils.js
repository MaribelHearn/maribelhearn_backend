const C = require("./constants")

/**
 * Convert raw PIV stored in the replay to PIV shown and used by point items
 * @param {*} gameId ID of the game
 * @param {*} rawPIV PIV stored in the replay
 * @returns real PIV used
 */
function convertToRealPIV(gameId, rawPIV) {
    switch (gameId) {
        // Return PIV * 10 for th10
        case C.GAME.TH10.ID:
            return rawPIV * 10
        // Return PIV * 10 for th12 onwards
        // "piv is stored with extra precision, we trunctate the value to what is shown ingame"
        case C.GAME.TH12.ID:
        case C.GAME.TH13.ID:
        case C.GAME.TH14.ID:
        case C.GAME.TH15.ID:
        case C.GAME.TH16.ID:
        case C.GAME.TH17.ID:
        case C.GAME.TH18.ID:
            return Math.trunc(rawPIV / 1000) * 10
        // Return default value for other games
        default:
            return rawPIV
    }
}

module.exports = {
    convertToRealPIV,
}