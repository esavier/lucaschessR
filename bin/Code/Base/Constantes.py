WHITE, BLACK = True, False

ST_PLAYING, ST_ENDGAME, ST_WAITING, ST_PAUSE = range(4)

# GAME TYPE
(
    GT_COMPETITION_WITH_TUTOR,
    GT_POSITIONS,
    GT_AGAINST_PGN,
    GT_AGAINST_ENGINE,
    GT_AGAINST_CHILD_ENGINE,
    GT_AGAINST_GM,
    GT_ALONE,
    GT_ELO,
    GT_MICELO,
    GT_FICS,
    GT_FIDE,
    GT_LICHESS,
    GT_ALBUM,
    GT_BOOK,
    GT_OPENINGS,
    GT_OPENING_LINES,
    GT_TACTICS,
    GT_RESISTANCE,
    GT_TOURNEY_ENGINES,
    GT_WORLD_MAPS,
    GT_ROUTES,
    GT_TURN_ON_LIGHTS,
    GT_WASHING_CREATE,
    GT_WASHING_TACTICS,
    GT_WASHING_REPLAY,
    GT_SINGULAR_MOVES,
    GT_NOTE_DOWN,
    GT_BMT
) = range(28)

OUT_NORMAL, OUT_REINIT = range(2)

# RESULTS
(
    RS_WIN_PLAYER,
    RS_WIN_OPPONENT,
    RS_DRAW,
    RS_DRAW_REPETITION,
    RS_DRAW_50,
    RS_DRAW_MATERIAL,
    RS_WIN_PLAYER_TIME,
    RS_WIN_OPPONENT_TIME,
    RS_UNKNOWN,
    RS_WIN_WHITE,
    RS_WIN_BLACK,
) = range(11)

RESULT_UNKNOWN, RESULT_WIN_WHITE, RESULT_WIN_BLACK, RESULT_DRAW = ("*", "1-0", "0-1", "1/2-1/2")

(
    TERMINATION_MATE,
    TERMINATION_DRAW_STALEMATE,
    TERMINATION_DRAW_REPETITION,
    TERMINATION_DRAW_MATERIAL,
    TERMINATION_DRAW_50,
    TERMINATION_DRAW_AGREEMENT,
    TERMINATION_RESIGN,
    TERMINATION_ADJUDICATION,
    TERMINATION_WIN_ON_TIME,
    TERMINATION_UNKNOWN,
) = ("MT", "DS", "DR", "DM", "D5", "DA", "RS", "AD", "LT", "UN")

BEEP_WIN_PLAYER = "GANAMOS"
BEEP_WIN_OPPONENT = "GANARIVAL"
BEEP_DRAW = "TABLAS"
BEEP_DRAW_REPETITION = "TABLASREPETICION"
BEEP_DRAW_50 = "TABLAS50"
BEEP_DRAW_MATERIAL = "TABLASFALTAMATERIAL"
BEEP_WIN_PLAYER_TIME = ("GANAMOSTIEMPO",)
BEEP_WIN_OPPONENT_TIME = "GANARIVALTIEMPO"

GO_FORWARD, GO_BACK, GO_START, GO_END, GO_FREE, GO_CLOCK = range(6)

# TOOLBAR
(
    TB_QUIT,
    TB_PLAY,
    TB_COMPETE,
    TB_TRAIN,
    TB_OPTIONS,
    TB_INFORMATION,
    TB_FILE,
    TB_SAVE,
    TB_SAVE_AS,
    TB_OPEN,
    TB_RESIGN,
    TB_REINIT,
    TB_TAKEBACK,
    TB_ADJOURN,
    TB_Adjournments,
    TB_END_GAME,
    TB_CLOSE,
    TB_PREVIOUS,
    TB_NEXT,
    TB_PASTE_PGN,
    TB_READ_PGN,
    TB_PGN_LABELS,
    TB_OTHER_GAME,
    TB_MY_GAMES,
    TB_DRAW,
    TB_BOXROOMS_PGN,
    TB_END,
    TB_SLOW,
    TB_PAUSE,
    TB_CONTINUE,
    TB_FAST,
    TB_REPEAT,
    TB_PGN,
    TB_HELP,
    TB_LEVEL,
    TB_ACCEPT,
    TB_CANCEL,
    # TB_GAME_OF_THE_DAY,
    TB_CONFIG,
    TB_UTILITIES,
    TB_VARIATIONS,
    TB_TOOLS,
    TB_CHANGE,
    TB_SHOW_TEXT,
    TB_HELP_TO_MOVE,
    TB_SEND,
    TB_STOP,
) = range(46)


ZVALUE_PIECE, ZVALUE_PIECE_MOVING = 10, 20

POS_TUTOR_HORIZONTAL, POS_TUTOR_HORIZONTAL_2_1, POS_TUTOR_HORIZONTAL_1_2, POS_TUTOR_VERTICAL = range(4)

MENU_PLAY_BOTH, MENU_PLAY_ANY_ENGINE, MENU_PLAY_YOUNG_PLAYERS = range(3)

(
    ADJUST_BETTER,
    ADJUST_SOMEWHAT_BETTER,
    ADJUST_SIMILAR,
    ADJUST_WORSE,
    ADJUST_WORST_MOVE,
    ADJUST_SELECTED_BY_PLAYER,
    ADJUST_HIGH_LEVEL,
    ADJUST_INTERMEDIATE_LEVEL,
    ADJUST_LOW_LEVEL,
    ADJUST_SOMEWHAT_BETTER_MORE,
    ADJUST_SOMEWHAT_BETTER_MORE_MORE,
    ADJUST_SOMEWHAT_WORSE_LESS,
    ADJUST_SOMEWHAT_WORSE_LESS_LESS,
) = range(13)

BLINDFOLD_NO, BLINDFOLD_CONFIG, BLINDFOLD_WHITE, BLINDFOLD_BLACK, BLINDFOLD_ALL = range(5)

KIBRUN_CONFIGURATION, KIBRUN_GAME, KIBRUN_CLOSE, KIBRUN_COPYCLIPBOARD, KIBRUN_STOP = ("C", "F", "T", "B", "S")

KIB_CANDIDATES = "M"
KIB_BESTMOVE = "S"
KIB_INDEXES = "I"
KIB_BESTMOVE_ONELINE = "L"
KIB_STOCKFISH = "E"
KIB_POLYGLOT = "B"
KIB_GAVIOTA = "G"
KIB_THREATS = "C"

FEN_INITIAL = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

NAG_0, NAG_1, NAG_2, NAG_3, NAG_4, NAG_5, NAG_6 = (
    NO_RATING,
    GOOD_MOVE,
    BAD_MOVE,
    VERY_GOOD_MOVE,
    VERY_POOR_MOVE,
    SPECULATIVE_MOVE,
    QUESTIONABLE_MOVE,
) = range(7)


dicHTMLnags = {
    NAG_1: "!",
    NAG_2: "?",
    NAG_3: "‼",
    NAG_4: "⁇",
    NAG_5: "⁉",
    NAG_6: "⁈",
    7: "□",
    10: "=",
    13: "∞",
    14: "⩲",
    15: "⩱",
    16: "±",
    17: "∓",
    18: "+-",
    19: "-+",
    22: "⨀",
    23: "⨀",
    32: "⟳",
    33: "⟳",
    36: "→",
    37: "→",
    40: "↑",
    41: "↑",
    132: "⇆",
    133: "⇆",
    140: "∆",
    142: "⌓",
    239: "⇔",
    240: "⇗",
    242: "⟫",
    243: "⟪",
    244: "✕",
    245: "⊥",
}

dicHTMLnagsTxt = {
    NAG_1: "!",
    NAG_2: "?",
    NAG_3: "!!",
    NAG_4: "??",
    NAG_5: "!?",
    NAG_6: "?!",
}




OPENING, MIDDLEGAME, ENDGAME, ALLGAME = range(4)

CALCWEIGHT_NUMGAMES, CALCWEIGHT_SCORE, CALCWEIGHT_NUMGAMES_SCORE = "NG", "SC100", "NGS"

STANDARD_TAGS = [
    "Event",
    "Site",
    "Date",
    "Round",
    "White",
    "Black",
    "Result",
    "WhiteTitle",
    "BlackTitle",
    "WhiteElo",
    "BlackElo",
    "WhiteUSCF",
    "WhiteFideID",
    "BlackFideID",
    "BlackUSCF",
    "WhiteNA",
    "BlackNA",
    "WhiteType",
    "BlackType",
    "EventDate",
    "EventSponsor",
    "ECO",
    "UTCTime",
    "UTCDate",
    "TimeControl",
    "TimeStart",
    "TimeEnd",
    "SetUp",
    "FEN",
    "PlyCount",
    "Section",
    "Stage",
    "Board",
    "Opening",
    "Variation",
    "SubVariation",
    "NIC",
    "Time",
    "Termination",
    "Annotator",
    "Mode",
]


TACTICS_BASIC, TACTICS_PERSONAL = "B", "P"

ALL, NONE, ONLY_WHITE, ONLY_BLACK = "A", "N", "W", "B"