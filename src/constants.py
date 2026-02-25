"""Constants for layout, colors, and game parameters."""

# ── Window ─────────────────────────────────────────────────────────────────────
WINDOW_WIDTH  = 520
WINDOW_HEIGHT = 720
TITLE         = "Wordle"
FPS           = 30

# ── Colors ─────────────────────────────────────────────────────────────────────
BG              = (255, 255, 255)
BLACK           = (0,   0,   0)
DARK_LINE       = (228, 228, 228)

# Tile states
TILE_BORDER_EMPTY  = (211, 214, 218)
TILE_BORDER_FILLED = (135, 138, 140)
CORRECT            = (106, 170, 100)   # green  – right letter, right spot
PRESENT            = (201, 180, 88)    # yellow – right letter, wrong spot
ABSENT             = (120, 124, 126)   # gray   – letter not in word

# Keyboard
KEY_DEFAULT = (211, 214, 218)

# Text
TEXT_LIGHT = (255, 255, 255)
TEXT_DARK  = (0,   0,   0)

# Toast messages
TOAST_BG   = (0,   0,   0)
TOAST_TEXT = (255, 255, 255)

# ── Grid ───────────────────────────────────────────────────────────────────────
CELL_SIZE = 62
CELL_GAP  = 5
GRID_COLS = 5
GRID_ROWS = 6
GRID_LEFT = (WINDOW_WIDTH - (GRID_COLS * CELL_SIZE + (GRID_COLS - 1) * CELL_GAP)) // 2
GRID_TOP  = 65

# ── On-screen keyboard ─────────────────────────────────────────────────────────
KEY_W     = 43
KEY_H     = 58
KEY_GAP   = 6
KB_TOP    = GRID_TOP + GRID_ROWS * (CELL_SIZE + CELL_GAP) + 18

KB_ROWS = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    ["ENTER"] + list("ZXCVBNM") + ["⌫"],
]

WIDE_KEYS  = {"ENTER", "⌫"}
WIDE_KEY_W = KEY_W + KEY_W // 2 + KEY_GAP // 2

# ── Letter-state constants ─────────────────────────────────────────────────────
S_CORRECT = "correct"
S_PRESENT = "present"
S_ABSENT  = "absent"

STATE_COLOR = {
    S_CORRECT: CORRECT,
    S_PRESENT: PRESENT,
    S_ABSENT:  ABSENT,
}

STATE_PRIORITY = {S_CORRECT: 2, S_PRESENT: 1, S_ABSENT: 0}
