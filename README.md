# Wordle Clone (Python + Pygame)

A fully playable Wordle clone built with Python and Pygame.

## Features

- 6×5 guess grid with colour feedback (green / yellow / gray)
- On-screen QWERTY keyboard (clickable) + physical keyboard input
- Proper duplicate-letter handling
- Random answer chosen from `data/answers.txt` on every run
- Guesses validated against `data/allowed.txt` (+ answers)
- Toast messages for invalid input and win/loss results
- Restart with **R** key (or **Enter** after the game ends)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/dmoney25632/worldeclone.git
cd worldeclone

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
python -m src
```

## How to Play

| Action | Control |
|--------|---------|
| Type a letter | **A–Z** key or click an on-screen key |
| Delete last letter | **Backspace** or click **⌫** |
| Submit guess | **Enter** or click **ENTER** |
| Restart | **R** (any time) or **Enter** after game ends |

### Colour Guide

| Colour | Meaning |
|--------|---------|
| 🟩 Green | Correct letter, correct position |
| 🟨 Yellow | Letter is in the word but in the wrong position |
| ⬜ Gray | Letter is not in the word |

## Project Structure

```
worldeclone/
├── data/
│   ├── answers.txt     # Pool of target words (5-letter)
│   └── allowed.txt     # Additional valid guess words (5-letter)
├── src/
│   ├── __init__.py
│   ├── __main__.py     # Entry point  (python -m src)
│   ├── constants.py    # Colors, layout sizes
│   ├── game.py         # Game logic & state
│   └── main.py         # Pygame rendering & event loop
├── requirements.txt
└── README.md
```
