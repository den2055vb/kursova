# ui_manager.py
import pygame
# Змінено SCREEN_WIDTH/HEIGHT на LOGICAL_WIDTH/HEIGHT
from constants import (LOGICAL_WIDTH, LOGICAL_HEIGHT, BG_COLOR, WHITE, LIGHT_GREY, HOVER_GREY,
                       MAX_NAME_LENGTH, MENU_OPTIONS_COUNT)

def draw_text(screen, text, font, color, center_x, center_y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)
    return text_rect 

def display_main_menu(screen, assets, selected_option_index=0, is_fullscreen_active=False):
    screen.fill(BG_COLOR)
    # Використовуємо LOGICAL_WIDTH/HEIGHT для позиціонування
    draw_text(screen, "Пін-Понг", assets.title_font, LIGHT_GREY, LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 5)

    fullscreen_toggle_text = "3. Вимкнути повний екран" if is_fullscreen_active else "3. Увімкнути повний екран"
    options_texts = ["1. Грати проти Бота", "2. Грати удвох", fullscreen_toggle_text]
    
    option_rects = [] 

    for i, option_text in enumerate(options_texts):
        color = HOVER_GREY if i == selected_option_index else WHITE 
        # Використовуємо LOGICAL_WIDTH/HEIGHT для позиціонування
        rect = draw_text(screen, option_text, assets.menu_item_font, color, 
                         LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 2 - 60 + i * 70) 
        option_rects.append(rect)

    # Використовуємо LOGICAL_WIDTH/HEIGHT для позиціонування
    draw_text(screen, "СТРІЛКИ/МИША - вибір, ENTER/КЛІК - підтвердити, F11 - повний екран",
              assets.small_message_font, LIGHT_GREY, LOGICAL_WIDTH / 2, LOGICAL_HEIGHT * 0.8)
    draw_text(screen, "Q - Вихід", assets.small_message_font, LIGHT_GREY, LOGICAL_WIDTH / 2, LOGICAL_HEIGHT * 0.8 + 40)
    
    return option_rects

def handle_main_menu_input_keyboard(event, selected_option_index):
    # ... (логіка залишається такою ж, вона не залежить від розмірів екрану) ...
    action = None
    new_index = selected_option_index

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            new_index = (selected_option_index - 1 + MENU_OPTIONS_COUNT) % MENU_OPTIONS_COUNT
        elif event.key == pygame.K_DOWN:
            new_index = (selected_option_index + 1) % MENU_OPTIONS_COUNT
        elif event.key == pygame.K_RETURN: 
            if new_index == 0: action = "vs_bot"
            elif new_index == 1: action = "pvp"
            elif new_index == 2: action = "toggle_fullscreen"
        elif event.key == pygame.K_q: 
             action = "quit"
        elif event.key == pygame.K_1: 
            new_index = 0
            action = "vs_bot"
        elif event.key == pygame.K_2: 
            new_index = 1
            action = "pvp"
        elif event.key == pygame.K_3: 
            new_index = 2
            action = "toggle_fullscreen"
            
    return new_index, action

def display_name_input(screen, assets, prompt_message, current_text, input_box_active):
    screen.fill(BG_COLOR)
    # Використовуємо LOGICAL_WIDTH/HEIGHT для позиціонування
    draw_text(screen, prompt_message, assets.menu_item_font, LIGHT_GREY, 
              LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 3)

    # Використовуємо LOGICAL_WIDTH/HEIGHT для позиціонування
    input_box_rect = pygame.Rect(LOGICAL_WIDTH / 2 - 200, LOGICAL_HEIGHT / 2 - 25, 400, 50)
    color = WHITE if input_box_active else LIGHT_GREY
    pygame.draw.rect(screen, color, input_box_rect, 2) 

    draw_text(screen, current_text, assets.input_font, WHITE, 
              LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 2)
    
    if input_box_active and (pygame.time.get_ticks() // 500) % 2 == 0:
        text_surface_for_cursor = assets.input_font.render(current_text, True, WHITE)
        # Розрахунок позиції курсора відносно input_box_rect, який вже відцентрований
        # тому не потрібно прямо використовувати LOGICAL_WIDTH тут, а відносно input_box_rect
        cursor_pos_x = input_box_rect.x + text_surface_for_cursor.get_width() + 5 
        if not current_text: # Якщо текст порожній, курсор по центру input_box
             text_width, _ = assets.input_font.size(" ") # Орієнтовна ширина для центрування
             cursor_pos_x = input_box_rect.centerx - text_width / 2 # Приблизно по центру
        pygame.draw.line(screen, WHITE, (cursor_pos_x, input_box_rect.y + 10), 
                         (cursor_pos_x, input_box_rect.y + input_box_rect.height - 10), 2)

    # Використовуємо LOGICAL_WIDTH/HEIGHT для позиціонування
    draw_text(screen, "Натисніть ENTER для підтвердження", assets.small_message_font, LIGHT_GREY,
              LOGICAL_WIDTH / 2, LOGICAL_HEIGHT * 0.7)

def handle_name_input_text(event, current_text):
    # ... (логіка залишається такою ж) ...
    name_confirmed = False
    new_text = current_text

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if len(new_text.strip()) > 0: 
                name_confirmed = True
        elif event.key == pygame.K_BACKSPACE:
            new_text = new_text[:-1]
        else:
            if len(new_text) < MAX_NAME_LENGTH:
                char = event.unicode
                if char.isalnum() or char in " _-": 
                    new_text += char
    return new_text, name_confirmed

def display_game_over_message(screen, assets, winner_name):
    # Використовуємо LOGICAL_WIDTH/HEIGHT для позиціонування
    draw_text(screen, f"{winner_name} переміг!", assets.score_font, LIGHT_GREY,
              LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 2 - 60)
    draw_text(screen, "ПРОБІЛ - грати знову", assets.small_message_font, WHITE,
              LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 2 + 20)
    draw_text(screen, "M - Головне меню", assets.small_message_font, WHITE,
              LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 2 + 60)
    draw_text(screen, "Q - Вихід", assets.small_message_font, WHITE,
              LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 2 + 100)

def handle_game_over_input(event):
    # ... (логіка залишається такою ж) ...
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            return "replay"
        elif event.key == pygame.K_m:
            return "main_menu"
        elif event.key == pygame.K_q:
            return "quit"
    return None