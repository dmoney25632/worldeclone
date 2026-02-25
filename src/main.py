"""Pygame rendering and main event loop for the Wordle clone."""

import sys
import pygame

from .constants import (
    BG, BLACK, DARK_LINE,
    TILE_BORDER_EMPTY, TILE_BORDER_FILLED,
    CORRECT, PRESENT, ABSENT,
    KEY_DEFAULT, TEXT_LIGHT, TEXT_DARK,
    TOAST_BG, TOAST_TEXT,
    WINDOW_WIDTH, WINDOW_HEIGHT, TITLE, FPS,
    CELL_SIZE, CELL_GAP, GRID_COLS, GRID_ROWS, GRID_LEFT, GRID_TOP,
    KEY_W, KEY_H, KEY_GAP, KB_TOP, KB_ROWS, WIDE_KEYS, WIDE_KEY_W,
    S_CORRECT, S_PRESENT, STATE_COLOR,
)
from .game import Game


# ── Drawing helpers ────────────────────────────────────────────────────────────

def _cell_rect(row: int, col: int) -> pygame.Rect:
    x = GRID_LEFT + col * (CELL_SIZE + CELL_GAP)
    y = GRID_TOP  + row * (CELL_SIZE + CELL_GAP)
    return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)


def _draw_grid(surface: pygame.Surface, game: Game, font: pygame.font.Font) -> None:
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = _cell_rect(row, col)

            if row < len(game.guesses):
                # Submitted guess – coloured tile
                ch    = game.guesses[row][col]
                state = game.states[row][col]
                color = STATE_COLOR[state]
                pygame.draw.rect(surface, color, rect, border_radius=2)
                txt = font.render(ch, True, TEXT_LIGHT)
                surface.blit(txt, txt.get_rect(center=rect.center))

            elif row == len(game.guesses) and not game.over:
                # Active row – show typed letters
                pygame.draw.rect(surface, BG, rect)
                if col < len(game.current):
                    ch = game.current[col]
                    pygame.draw.rect(surface, TILE_BORDER_FILLED, rect, 2)
                    txt = font.render(ch, True, BLACK)
                    surface.blit(txt, txt.get_rect(center=rect.center))
                else:
                    pygame.draw.rect(surface, TILE_BORDER_EMPTY, rect, 2)

            else:
                # Empty future row
                pygame.draw.rect(surface, BG, rect)
                pygame.draw.rect(surface, TILE_BORDER_EMPTY, rect, 2)


def _key_rect(row_idx: int, col_idx: int) -> pygame.Rect:
    """Return the screen rect for a key at *row_idx*, *col_idx*."""
    row = KB_ROWS[row_idx]
    total_w = sum(WIDE_KEY_W if k in WIDE_KEYS else KEY_W for k in row)
    total_w += KEY_GAP * (len(row) - 1)
    x_start = (WINDOW_WIDTH - total_w) // 2

    x = x_start
    for i, key in enumerate(row):
        kw = WIDE_KEY_W if key in WIDE_KEYS else KEY_W
        if i == col_idx:
            return pygame.Rect(x, KB_TOP + row_idx * (KEY_H + KEY_GAP), kw, KEY_H)
        x += kw + KEY_GAP
    raise ValueError(f"col_idx {col_idx} out of range for row {row_idx}")


def _draw_keyboard(surface: pygame.Surface, game: Game, font: pygame.font.Font) -> None:
    for ri, row in enumerate(KB_ROWS):
        for ci, key in enumerate(row):
            rect = _key_rect(ri, ci)
            if len(key) == 1:
                st = game.key_states.get(key)
                bg_color   = STATE_COLOR.get(st, KEY_DEFAULT)  # type: ignore[arg-type]
                txt_color  = TEXT_LIGHT if st is not None else TEXT_DARK
            else:
                bg_color  = KEY_DEFAULT
                txt_color = TEXT_DARK

            pygame.draw.rect(surface, bg_color, rect, border_radius=4)
            lbl = font.render(key, True, txt_color)
            surface.blit(lbl, lbl.get_rect(center=rect.center))


def _hit_key(pos: tuple[int, int]) -> str | None:
    """Return the key label at screen position *pos*, or None."""
    for ri, row in enumerate(KB_ROWS):
        for ci in range(len(row)):
            if _key_rect(ri, ci).collidepoint(pos):
                return KB_ROWS[ri][ci]
    return None


def _draw_toast(surface: pygame.Surface, text: str, font: pygame.font.Font) -> None:
    lbl     = font.render(text.upper(), True, TOAST_TEXT)
    pad     = 10
    bg_rect = pygame.Rect(0, 0, lbl.get_width() + pad * 2, lbl.get_height() + pad * 2)
    bg_rect.centerx = WINDOW_WIDTH // 2
    bg_rect.top     = GRID_TOP + 10
    pygame.draw.rect(surface, TOAST_BG, bg_rect, border_radius=6)
    surface.blit(lbl, lbl.get_rect(center=bg_rect.center))


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Arial", 28, bold=True)
    font_cell  = pygame.font.SysFont("Arial", 34, bold=True)
    font_key   = pygame.font.SysFont("Arial", 15, bold=True)
    font_toast = pygame.font.SysFont("Arial", 18, bold=True)
    font_hint  = pygame.font.SysFont("Arial", 14)

    game    = Game()
    running = True

    while running:
        ticks = pygame.time.get_ticks()

        # ── Events ─────────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif game.over and event.key == pygame.K_RETURN:
                    game.reset()
                elif event.key == pygame.K_RETURN:
                    game.submit(ticks)
                elif event.key == pygame.K_BACKSPACE:
                    game.delete_letter()
                elif event.unicode and event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    game.add_letter(event.unicode.upper())

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                key = _hit_key(event.pos)
                if key == "ENTER":
                    game.submit(ticks)
                elif key == "⌫":
                    game.delete_letter()
                elif key:
                    game.add_letter(key)

        # ── Draw ───────────────────────────────────────────────────────────────
        screen.fill(BG)

        # Title bar
        title_surf = font_title.render(TITLE.upper(), True, BLACK)
        screen.blit(title_surf, title_surf.get_rect(centerx=WINDOW_WIDTH // 2, y=12))
        pygame.draw.line(screen, DARK_LINE, (0, 52), (WINDOW_WIDTH, 52), 1)

        _draw_grid(screen, game, font_cell)
        _draw_keyboard(screen, game, font_key)

        # Toast message
        if game.message and ticks < game.msg_until:
            _draw_toast(screen, game.message, font_toast)

        # Restart hint
        if game.over:
            hint = font_hint.render("Press R (or Enter) to play again", True, ABSENT)
            screen.blit(hint, hint.get_rect(centerx=WINDOW_WIDTH // 2, bottom=WINDOW_HEIGHT - 8))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
