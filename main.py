import datetime
import os
import sys

from src.core.game_loop import game_loop
from src.core.game_state import GameState
from src.utils import constants as c

import pygame

# To create a standalone executable:
# pyinstaller --windowed --onedir --name "Snake"
# --icon=assets/images/icon-macos.icns --add-data "assets:assets" main.py


def get_resource_path() -> str:
    """
    Return the path to the resource directory.
    Works both for development and for PyInstaller bundles.
    """
    if getattr(sys, "frozen", False):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(sys.executable)
        return base_path
    return os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    """
    Main function to run the game.
    Creates a game state, initializes pygame, and runs the game loop.
    """
    try:
        base_path = get_resource_path()
        os.chdir(base_path)

        pygame.init()
        icon_path = os.path.join(base_path, "assets", "images", "icon.png")
        pygame.display.set_icon(pygame.image.load(icon_path))
        screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT), pygame.SCALED, vsync=1)
        pygame.display.set_caption("Sleepy Fox")
        clock = pygame.time.Clock()
        pygame.time.set_timer(c.BONUS_SPAWN_EVENT, c.BONUS_SPAWN_INTERVAL)

        game_state = GameState()
        game_loop(screen, game_state, clock)
    except Exception as e:
        error_path = os.path.join(os.path.expanduser('~'), 'sleepyfox_error.txt')
        with open(error_path, 'w') as f:
            f.write(f"Error occurred at {datetime.datetime.now()}\n")
            f.write(f"Error: {str(e)}\n")
            f.write(f"Base path: {base_path}\n")
            f.write(f"Current working directory: {os.getcwd()}\n")
            import traceback
            f.write(traceback.format_exc())
        print(f"An error occurred. Check {error_path} for details.", file=sys.stderr)
        import time
        time.sleep(5)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
