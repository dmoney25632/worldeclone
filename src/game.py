"""Pure game-logic: state, evaluation, and word loading."""

import os
import random

from .constants import (
    GRID_ROWS,
    S_ABSENT,
    S_CORRECT,
    S_PRESENT,
    STATE_PRIORITY,
)

# ── Word loading ───────────────────────────────────────────────────────────────
_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _load(filename: str) -> list[str]:
    path = os.path.join(_DATA_DIR, filename)
    with open(path, encoding="utf-8") as fh:
        return [w.strip().upper() for w in fh if len(w.strip()) == 5]


ANSWERS: list[str] = _load("answers.txt")
ALLOWED: set[str] = set(_load("allowed.txt")) | set(ANSWERS)


# ── Game ───────────────────────────────────────────────────────────────────────
class Game:
    """Holds all mutable state for one round of Wordle."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.target: str = random.choice(ANSWERS)
        self.guesses: list[str] = []
        self.states: list[list[str]] = []   # per-cell state for submitted rows
        self.current: str = ""
        self.over: bool = False
        self.won: bool = False
        self.message: str = ""
        self.msg_until: int = 0             # ticks until message disappears
        self.key_states: dict[str, str] = {}  # best state seen for each letter

    # ── input ──────────────────────────────────────────────────────────────────
    def add_letter(self, ch: str) -> None:
        if not self.over and len(self.current) < 5:
            self.current += ch.upper()

    def delete_letter(self) -> None:
        if not self.over:
            self.current = self.current[:-1]

    def submit(self, ticks: int) -> None:
        """Try to submit the current guess.  *ticks* is pygame.time.get_ticks()."""
        if self.over:
            return
        if len(self.current) < 5:
            self._set_msg("Not enough letters", ticks, 1500)
            return
        if self.current not in ALLOWED:
            self._set_msg("Not in word list", ticks, 1500)
            return

        row_states = self._evaluate(self.current)
        self.guesses.append(self.current)
        self.states.append(row_states)
        self._update_key_states(self.current, row_states)

        if self.current == self.target:
            self.won = True
            self.over = True
            labels = ["Genius!", "Magnificent!", "Impressive!", "Splendid!", "Great!", "Phew!"]
            self._set_msg(labels[len(self.guesses) - 1], ticks, 3000)
        elif len(self.guesses) == GRID_ROWS:
            self.over = True
            self._set_msg(self.target, ticks, 5000)

        self.current = ""

    # ── helpers ────────────────────────────────────────────────────────────────
    def _evaluate(self, guess: str) -> list[str]:
        result = [S_ABSENT] * 5
        remaining = list(self.target)

        # Pass 1 – correct positions
        for i, (g, t) in enumerate(zip(guess, remaining)):
            if g == t:
                result[i] = S_CORRECT
                remaining[i] = None  # type: ignore[assignment]

        # Pass 2 – present (wrong position)
        for i, g in enumerate(guess):
            if result[i] == S_CORRECT:
                continue
            if g in remaining:
                result[i] = S_PRESENT
                remaining[remaining.index(g)] = None  # type: ignore[assignment]

        return result

    def _update_key_states(self, guess: str, row_states: list[str]) -> None:
        for ch, st in zip(guess, row_states):
            prev = self.key_states.get(ch)
            if prev is None or STATE_PRIORITY[st] > STATE_PRIORITY[prev]:
                self.key_states[ch] = st

    def _set_msg(self, text: str, ticks: int, duration: int) -> None:
        self.message = text
        self.msg_until = ticks + duration
