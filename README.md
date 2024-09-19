https://github.com/user-attachments/assets/a6f6f4de-1288-4f4a-ad34-4036036940d5
![slotmachine](https://github.com/user-attachments/assets/1e8fda5c-751d-42d3-bd7c-d77ccb1d4fba)
# Slot Machine Game in Python (Tkinter)
# Description
This is a simple GUI-based slot machine game implemented in Python using the Tkinter library for the graphical user interface (GUI). The game simulates a slot machine with various symbols, allowing players to place bets and spin to win based on matching symbols.

# Features
1. Interactive slot machine game with a 3x3 grid.
2. Adjustable number of lines (up to 3) and bet amount per line.
3. Winning symbols:
• ❤️ (Heart)
• ♦️ (Diamond)
• ♣️ (Club)
• ♠️ (Spade)
• ✨ (Sparkle)
4. Sound effects for spinning and winning using the pygame library.
5. Flashing background for winning spins.
6. Simple betting and balance management.
7. Graphical interface created with Tkinter.

# Installation
# Prerequisites
1. Python 3.x
2. Tkinter (comes pre-installed with most Python distributions)
3. pygame library for sound effects
4. MP3 sound files for spinning and winning events (slotmachine.mp3 and won.mp3)

# Installing the pygame library:
You need to install the pygame package to handle sound effects. You can install it using pip: pip install pygame

# Running the Game
1. Clone or download this repository.
2. Make sure you have the required sound files (slotmachine.mp3 and won.mp3) placed in the same directory as the script.
3. Run the game by executing the following command: python gui.py

The game will start with an initial balance prompt where you can specify how much money you want to start with.

# How to Play
1. Enter your starting balance when prompted.
2. In the game window:
• Enter the number of lines to bet on (1-3).
• Enter the bet amount per line (minimum: 1, maximum: 100,000).
3. Click the Spin button to play.
4. If you win, your balance will increase based on the symbol values and your bet.
5. The game displays your total balance and winnings after each spin.
6. Press the Quit button to exit the game.

# Game Rules
• The slot machine has five types of symbols with different frequencies and payouts.
    • ❤️ (Heart): Most valuable (100x payout, appears less frequently)
    • ♦️ (Diamond): Medium value (50x payout)
    • ♣️ (Club): Low value (25x payout)
    • ♠️ (Spade): Lowest value (5x payout)
    • ✨ (Sparkle): Least valuable but rare (2x payout)
• If all the symbols in a line are the same, you win the corresponding value multiplied by your bet.

# License
This project is licensed under the MIT License - see the LICENSE file for details.
