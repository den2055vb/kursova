# main.py
import pygame
import sys # Для sys.exit()
# Імпортуємо GameManager після ініціалізації pygame
# from constants import * # Не потрібен тут, якщо GameManager все використовує
# from game_manager import GameManager # Перемістимо імпорт нижче

if __name__ == '__main__':
    pygame.init()
    pygame.font.init() # Хоча pygame.init() має це робити, явна ініціалізація не завадить

    # Імпортуємо GameManager ПІСЛЯ ініціалізації pygame,
    # особливо якщо GameManager або його залежності (як Assets)
    # використовують pygame.font при завантаженні модуля.
    from game_manager import GameManager

    game = GameManager()
    game.run_game_loop()

    pygame.quit()
    sys.exit()