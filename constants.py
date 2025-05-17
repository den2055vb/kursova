# constants.py
import pygame

# Розміри екрану (логічні, для дизайну гри)
LOGICAL_WIDTH = 800
LOGICAL_HEIGHT = 600

# Цільова роздільна здатність для повноекранного режиму
TARGET_FULLSCREEN_WIDTH = 1920
TARGET_FULLSCREEN_HEIGHT = 1080

# Кольори
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
LIGHT_GREY = pygame.Color('grey70') 
HOVER_GREY = pygame.Color('grey85') 
BG_COLOR = pygame.Color('grey12')

### НОВІ КОЛЬОРИ ДЛЯ ІГРОВИХ ОБ'ЄКТІВ ###
PLAYER1_COLOR = pygame.Color('blue')    # Синій для лівого гравця
PLAYER2_COLOR = pygame.Color('red')     # Червоний для правого гравця (або бота)
BALL_COLOR = pygame.Color('green')      # Зелений для м'яча
### ------------------------------------ ###

# Параметри м'яча
BALL_RADIUS = 10
BASE_BALL_SPEED_X = 6
BASE_BALL_SPEED_Y = 6
BALL_SPEED_INCREASE_FACTOR = 1.03 
MAX_BALL_SPEED_FACTOR = 2.5      

# Параметри ракеток
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ігрові параметри
WINNING_SCORE = 5
MAX_NAME_LENGTH = 12
MENU_OPTIONS_COUNT = 3 

# Розміри шрифтів
FONT_SIZE_TITLE = 90
FONT_SIZE_MENU_ITEM = 45
FONT_SIZE_SCORE = 70
FONT_SIZE_SMALL_MESSAGE = 30
FONT_SIZE_INPUT = 45

# Ігрові стани
STATE_MAIN_MENU = "STATE_MAIN_MENU"
STATE_NAME_INPUT_P1_BOT = "STATE_NAME_INPUT_P1_BOT"
STATE_NAME_INPUT_P1_PVP = "STATE_NAME_INPUT_P1_PVP"
STATE_NAME_INPUT_P2_PVP = "STATE_NAME_INPUT_P2_PVP"
STATE_GAMEPLAY = "STATE_GAMEPLAY"