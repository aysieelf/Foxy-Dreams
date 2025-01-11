# 🦊 Sleepy Fox User Guide

## Game Overview
Sleepy Fox is a classic Pong game with a twist.

Pong is a two-player sports game that simulates table tennis. 
Players control paddles on opposite sides of the screen, hitting a ball back and forth. 
The goal is to score points by making the ball pass the opponent's paddle.

## Getting Started
1. Launch the game by running `python main.py` or double-clicking the `SleepyFox` executable
2. Chose the game mode you want to play (Single Player or Multiplayer)
3. You can toggle sound and music on/off in the start screen
4. Click the "start game" button on the welcome screen to begin

## Game Interface
- **Start Screen**: The initial screen with the game title, start button, and settings buttons (game modes, sound on/off, music on/off)
- **Playing Screen**: The main game screen where the action takes place with score board and level indicator
- **Pause Screen**: The screen that appears when the game is paused, with options to resume or return to the main menu and settings buttons (sound on/off, music on/off)
- **Game Over Screen**: The screen that appears when the game ends, showing the final score and the leaderboard (date, score)

## How to Play
- Your goal is to prevent the fox from passing your cloud
- Use the arrow keys or WASD to move your cloud up and down
- The velocity of the fox is affected depending on the angle it hits the cloud - use this to your advantage
- Collect bonus stars for extra points and speed boosts
- With each level, the game gets faster and more challenging
- The game ends when you choose to quit

## Controls
- Single Player Mode:
  - Player 1 (Cloud): `W` (up) `S` (down)
  - Pause/Resume: `Space`
  - Return to Menu: `Esc`
- Multiplayer Mode:
  - Player 1 (Left Cloud): `W` (up) `S` (down)
  - Player 2 (Right Cloud): `↑` (up) `↓` (down)
  - Pause/Resume: `Space`
  - Return to Menu: `Esc`

## Game Features
- Single Player Mode
- Multiplayer Mode
- Sound Effects
- Background Music
- Pause/Resume Functionality
- Level Progression
- Bonus Star Collection
- Leaderboard
- Settings Menu
- Main Menu Navigation

## High Scores

The game automatically saves your high scores after each game. Scores are stored in:
* **macOS**: `~/Documents/SleepyFox/scores.pkl`
* **Windows**: `Documents\SleepyFox\scores.pkl`

The game keeps track of your top 5 scores, showing:
* The date and time when the score was achieved
* The number of points scored
* Scores from both single player and multiplayer games

If you want to back up your scores or transfer them to another computer, you can:
1. Copy the `scores.pkl` file from the above location
2. Place it in the same location on the new computer

## Tips for Playing
- Keep an eye on the fox's velocity to predict its movement
- Use the walls to your advantage to bounce the fox back
- Collect bonus stars for extra points

## Troubleshooting
**Game does not start:**
- Ensure Python 3.12+ is installed
- Check if PyGame is properly installed
- Verify all game files are present

**Can't control the cloud:**
- Make sure the game window is active
- Check if the arrow keys or W/S/UP/DOWN are functioning correctly
- Restart the game if the issue persists

**Game seems frozen:**
- Press the space bar to pause/resume the game
- Check if the game window is in focus
- Restart the game if necessary

**Game crashes or displays errors:**
- Check the terminal/console for error messages
- Verify that all game files are intact
- Restart the game and try again

## Need Help?
If you encounter any issues not covered in this guide, please:

1. Check the project's GitHub Issues page
2. Create a new issue with detailed problem description
3. Include your system information and error messages if any