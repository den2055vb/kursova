# assets.py
import pygame
from constants import FONT_SIZE_TITLE, FONT_SIZE_MENU_ITEM, FONT_SIZE_SCORE, FONT_SIZE_SMALL_MESSAGE, FONT_SIZE_INPUT

class Assets:
    def __init__(self):
        self.default_font_name = None # Використовуватиме стандартний шрифт Pygame
        # Або можна вказати шлях до файлу .ttf: self.default_font_name = "ва_шрифт.ttf"

        try:
            # Спробуємо завантажити шрифти. Font(None, size) використовує вбудований шрифт.
            self.title_font = pygame.font.Font(self.default_font_name, FONT_SIZE_TITLE)
            self.menu_item_font = pygame.font.Font(self.default_font_name, FONT_SIZE_MENU_ITEM)
            self.score_font = pygame.font.Font(self.default_font_name, FONT_SIZE_SCORE)
            self.small_message_font = pygame.font.Font(self.default_font_name, FONT_SIZE_SMALL_MESSAGE)
            self.input_font = pygame.font.Font(self.default_font_name, FONT_SIZE_INPUT)
            print("Шрифти успішно завантажено.")
        except Exception as e:
            print(f"Помилка завантаження шрифтів (Font(None...)): {e}. Спроба SysFont.")
            try:
                # Якщо Font(None, size) не спрацював, спробуємо системний шрифт
                self.title_font = pygame.font.SysFont('arial', FONT_SIZE_TITLE)
                self.menu_item_font = pygame.font.SysFont('arial', FONT_SIZE_MENU_ITEM)
                self.score_font = pygame.font.SysFont('arial', FONT_SIZE_SCORE)
                self.small_message_font = pygame.font.SysFont('arial', FONT_SIZE_SMALL_MESSAGE)
                self.input_font = pygame.font.SysFont('arial', FONT_SIZE_INPUT)
                print("Системні шрифти 'arial' завантажено.")
            except Exception as e_sys:
                print(f"Критична помилка: не вдалося завантажити жоден шрифт: {e_sys}")
                # У реальній грі тут може бути краща обробка або вихід
                raise SystemExit(f"Не вдалося завантажити шрифти: {e_sys}")

# Створюємо один екземпляр Assets, який буде імпортуватися іншими модулями,
# але тільки ПІСЛЯ pygame.font.init()
# Краще створювати об'єкт Assets в GameManager після ініціалізації pygame.
# Тому поки що цей файл містить лише клас.