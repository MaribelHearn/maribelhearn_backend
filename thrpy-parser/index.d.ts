export function parse(replay: Buffer): object
export function parse06(replay: Buffer): object
export function parse07(replay: Buffer): object
export function parse08(replay: Buffer): object
export function parse09(replay: Buffer): object
export function parse10(replay: Buffer): object
export function parse11(replay: Buffer): object
export function parse12(replay: Buffer): object
export function parse128(replay: Buffer): object
export function parse13(replay: Buffer): object
export function parse14(replay: Buffer): object
export function parse13or14(replay: Buffer): object
export function parse15(replay: Buffer): object
export function parse16(replay: Buffer): object
export function parse17(replay: Buffer): object
export function parse18(replay: Buffer): object

export const CONSTANTS: {
    NO_SPELL_CARD_ID: 0xFFFF,
    NO_SPELL_PRACTICE_ID: 0xFFFFFFFF,
    GAME: {
        TH06: {
            ID: "th06",
            MAGIC: "T6RP"
        },
        TH07: {
            ID: "th07",
            MAGIC: "T7RP"
        },
        TH08: {
            ID: "th08",
            MAGIC: "T8RP"
        },
        TH09: {
            ID: "th09",
            MAGIC: "T9RP"
        },
        TH10: {
            ID: "th10",
            MAGIC: "t10r"
        },
        TH11: {
            ID: "th11",
            MAGIC: "t11r"
        },
        TH12: {
            ID: "th12",
            MAGIC: "t12r"
        },
        TH128: {
            ID: "th128",
            MAGIC: "128r"
        },
        TH13: {
            ID: "th13",
            MAGIC: "t13r"
        },
        TH14: {
            ID: "th14",
            MAGIC: "t13r"
        },
        TH15: {
            ID: "th15",
            MAGIC: "t15r"
        },
        TH16: {
            ID: "th16",
            MAGIC: "t16r"
        },
        TH17: {
            ID: "th17",
            MAGIC: "t17r"
        },
        TH18: {
            ID: "th18",
            MAGIC: "t18r"
        },
    },
    DIFFICULTY: {
        EASY: 0,
        NORMAL: 1,
        HARD: 2,
        LUNATIC: 3,
        EXTRA: 4,
        PHANTASM: 5,
    },
    REPLAY_TYPE: {
        FULL_GAME: 0,
        STAGE_PRACTICE: 1,
        SPELL_PRACTICE: 2,
        PVP: 3,
    },
}