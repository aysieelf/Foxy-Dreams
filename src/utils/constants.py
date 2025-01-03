# GAME LOOP --------------------------------------------------------------------
import pygame

FPS = 60

# WINDOW -----------------------------------------------------------------------
WIDTH = 640
HEIGHT = 480

# FOX -------------------------------------------------------------------------
BASE_SPEED = 6
MAX_SPEED = 20
FOX_HITBOX_DIFF = 15

# CLOUD -----------------------------------------------------------------------
# PLAYER1
CLOUD_PLAYER1_X = 5
CLOUD_PLAYER1_ROTATION = 270

# PLAYER2
CLOUD_PLAYER2_X = WIDTH - 48
CLOUD_PLAYER2_ROTATION = 90

CLOUD_Y = HEIGHT // 2
CLOUD_HITBOX_WIDTH_DIFF = 26
CLOUD_HITBOX_HEIGHT_DIFF = 0

# BONUS STAR ------------------------------------------------------------------
# We set something like IDs for the events
BONUS_SPAWN_EVENT = (
    pygame.USEREVENT + 1
)  # (32769) - a special event type with number 32768
BONUS_DE_SPAWN_EVENT = pygame.USEREVENT + 2  # (32770)
BONUS_SPAWN_INTERVAL = 20 * 1000  # 20 * 1000 milliseconds
BONUS_LIFETIME = 5 * 1000  # 5 * 1000 milliseconds
BONUS_POINTS = 2
BONUS_HITBOX_DIFF = 5

# COLORS -----------------------------------------------------------------------
STAR_PARTICLES_COLOR = (249, 182, 154)  # for particles
WARM_GREY = (155, 155, 155)
WHITE = (255, 255, 255)

# START SCREEN -----------------------------------------------------------------
# Title
TITLE_FONT = "impact"
TITLE_FONT_SIZE = 50
TITLE_TEXT = "SNAKE"
TITLE_COLOR = WARM_GREY
TITLE_Y_POS = 80

# Start Button
START_BUTTON_TEXT = "start game"
START_BUTTON_WIDTH = 180
START_BUTTON_HEIGHT = 50
START_BUTTON_TITLE_COLOR = WARM_GREY
START_BUTTON_TITLE_HOVER_COLOR = WHITE
START_BUTTON_COLOR = WARM_GREY
START_BUTTON_HOVER_COLOR = WHITE
START_BUTTON_FONT_SIZE = 35

# GAME OVER SCREEN -------------------------------------------------------------
GAME_OVER_FONT_SIZE = 48
GAME_OVER_FONT = "impact"
GAME_OVER_TEXT = "GAME OVER"
GAME_OVER_TEXT_COLOR = WARM_GREY
GAME_OVER_TEXT_POS = 100
OVERLAY_ALPHA = 100

# INSTRUCTIONS -----------------------------------------------------------------
INSTRUCTIONS_FONT_SIZE = 14
INSTRUCTIONS_FONT = "arial"
INSTRUCTIONS_TEXT_0 = (
    "Use the arrow keys or WASD to move the snake"  # only in the start screen
)
INSTRUCTIONS_TEXT_1 = (
    "Press SPACE to start or pause/resume the game"  # only in the start screen
)
INSTRUCTIONS_TEXT_2 = "Press Q to quit the game"  # only in the game over screen
INSTRUCTIONS_TEXT_3 = "Press R to restart"  # only in the game over screen
INSTRUCTIONS_TEXT_4 = "Press Q to quit to main menu"  # only in the game over screen
INSTRUCTIONS_TEXT_5 = "Press Q again to quit the game"  # only in the start screen
INSTRUCTIONS_TEXT_COLOR = WARM_GREY
INSTRUCTIONS = [
    INSTRUCTIONS_TEXT_0,
    INSTRUCTIONS_TEXT_1,
    INSTRUCTIONS_TEXT_2,
    INSTRUCTIONS_TEXT_3,
    INSTRUCTIONS_TEXT_4,
    INSTRUCTIONS_TEXT_5,
]
INSTRUCTIONS_POS = 170

# SCOREBOARD -------------------------------------------------------------------
SCORE_FONT_SIZE = 20
SCORE_FONT = "arial bold"
SCORE_TEXT = "SCORE: "
SCORE_PADDING = 5
