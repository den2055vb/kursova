# game_manager.py
import pygame
import sys
from constants import * # Імпортуємо всі константи, включаючи нові кольори
from assets import Assets
from game_objects import Paddle, Ball
import bot 
import ui_manager 

class GameManager:
    def __init__(self):
        self.desktop_info = pygame.display.Info() 
        self.target_fullscreen_width = TARGET_FULLSCREEN_WIDTH 
        self.target_fullscreen_height = TARGET_FULLSCREEN_HEIGHT
        
        self.is_fullscreen = False 
        self.logical_surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))
        
        self.scale_factor = 1.0
        self.scaled_width = LOGICAL_WIDTH
        self.scaled_height = LOGICAL_HEIGHT
        self.offset_x = 0
        self.offset_y = 0

        self.update_screen_mode() 

        pygame.display.set_caption('Пін-Понг Pro V2 - Кольори!') # Можете оновити заголовок
        self.clock = pygame.time.Clock()
        self.assets = Assets() 

        # Ігрові об'єкти створюються з новими кольорами
        self.player1 = Paddle(30, LOGICAL_HEIGHT / 2 - PADDLE_HEIGHT / 2, 
                              PADDLE_WIDTH, PADDLE_HEIGHT, 
                              PLAYER1_COLOR, # ### ЗМІНЕНО ###
                              PADDLE_SPEED, "Гравець 1")
        
        self.player2 = Paddle(LOGICAL_WIDTH - 30 - PADDLE_WIDTH, LOGICAL_HEIGHT / 2 - PADDLE_HEIGHT / 2, 
                              PADDLE_WIDTH, PADDLE_HEIGHT, 
                              PLAYER2_COLOR, # ### ЗМІНЕНО ###
                              PADDLE_SPEED, "Гравець 2") # Ім'я "Гравець 2" буде змінено на "Бот", якщо обрано режим гри з ботом
        
        self.ball = Ball(LOGICAL_WIDTH / 2, LOGICAL_HEIGHT / 2, 
                         BALL_RADIUS, 
                         BALL_COLOR,      # ### ЗМІНЕНО ###
                         BASE_BALL_SPEED_X, BASE_BALL_SPEED_Y)

        # ... (решта коду __init__ залишається без змін) ...
        self.current_state = STATE_MAIN_MENU
        self.is_running = True
        self.game_active = False 
        self.winner = None
        self.play_against_bot = False
        self.menu_selected_option = 0
        self.menu_option_rects = [] 
        self.name_input_text = ""
        self.name_input_active = True
        self.current_player_to_name_idx = 1

    # ... (решта методів класу GameManager: update_screen_mode, toggle_fullscreen, 
    # _handle_global_events, _process_input, _update_logic, _process_collisions, 
    # _process_scoring, _render_gameplay, _render, change_state, 
    # start_new_game_session, run_game_loop - залишаються такими ж, як у попередньому варіанті) ...
    # (скопіюйте їх з попередньої відповіді, де ми додавали масштабований повноекранний режим)

    def update_screen_mode(self):
        current_caption = "Пін-Понг Pro V2 - Кольори!"
        if pygame.display.get_init() and pygame.display.get_active():
             caption_info = pygame.display.get_caption()
             if caption_info and caption_info[0]: 
                 current_caption = caption_info[0]

        screen_flags = 0
        if self.is_fullscreen:
            print(f"Спроба увімкнути повноекранний режим: {self.target_fullscreen_width}x{self.target_fullscreen_height}")
            screen_flags = pygame.FULLSCREEN
            try:
                self.screen = pygame.display.set_mode((self.target_fullscreen_width, self.target_fullscreen_height), screen_flags)
            except pygame.error as e:
                print(f"Помилка встановлення повноекранного режиму {self.target_fullscreen_width}x{self.target_fullscreen_height}: {e}. Спроба нативної роздільної.")
                try: 
                    self.screen = pygame.display.set_mode((self.desktop_info.current_w, self.desktop_info.current_h), screen_flags)
                except pygame.error as e2:
                    print(f"Помилка встановлення нативної повноекранної роздільної: {e2}. Повернення до віконного.")
                    self.is_fullscreen = False 
                    self.update_screen_mode() 
                    return 
        else: 
            print(f"Встановлення віконного режиму: {LOGICAL_WIDTH}x{LOGICAL_HEIGHT}")
            screen_flags = pygame.RESIZABLE
            self.screen = pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT), screen_flags)
        
        pygame.display.set_caption(current_caption)
        self._calculate_scale_and_offsets() 
        print(f"Режим екрану оновлено. Повний екран: {self.is_fullscreen}. Розмір вікна: {self.screen.get_size()}")


    def _calculate_scale_and_offsets(self):
        physical_width, physical_height = self.screen.get_size()
        
        ratio_logical = LOGICAL_WIDTH / LOGICAL_HEIGHT
        ratio_physical = physical_width / physical_height

        if ratio_physical > ratio_logical: 
            self.scaled_height = physical_height
            self.scaled_width = int(self.scaled_height * ratio_logical)
        else: 
            self.scaled_width = physical_width
            self.scaled_height = int(self.scaled_width / ratio_logical)
        
        self.scale_factor = self.scaled_height / LOGICAL_HEIGHT 
        
        self.offset_x = (physical_width - self.scaled_width) // 2
        self.offset_y = (physical_height - self.scaled_height) // 2


    def _get_logical_mouse_pos(self, physical_mouse_pos):
        if self.scaled_width == 0 or self.scaled_height == 0 : 
            return (-1, -1)

        if not (self.offset_x <= physical_mouse_pos[0] < self.offset_x + self.scaled_width and \
                self.offset_y <= physical_mouse_pos[1] < self.offset_y + self.scaled_height):
            return (-1, -1) 

        logical_x = int((physical_mouse_pos[0] - self.offset_x) * (LOGICAL_WIDTH / self.scaled_width))
        logical_y = int((physical_mouse_pos[1] - self.offset_y) * (LOGICAL_HEIGHT / self.scaled_height))
        return (logical_x, logical_y)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.update_screen_mode()

    def _handle_global_events(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: 
                 if self.current_state != STATE_MAIN_MENU:
                     self.change_state(STATE_MAIN_MENU)
            elif event.key == pygame.K_F11: 
                self.toggle_fullscreen()
        if not self.is_fullscreen and event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self._calculate_scale_and_offsets() 
            print(f"Розмір вікна змінено на: {event.w}x{event.h}")


    def _process_input(self):
        key_action = None 
        mouse_click_action = None 
        physical_mouse_pos = pygame.mouse.get_pos() 
        logical_mouse_pos = self._get_logical_mouse_pos(physical_mouse_pos) 

        for event in pygame.event.get():
            self._handle_global_events(event) 
            if not self.is_running: return

            current_event_logical_mouse_pos = self._get_logical_mouse_pos(event.pos) if hasattr(event, 'pos') else logical_mouse_pos

            if self.current_state == STATE_MAIN_MENU:
                new_selection_key, key_action_from_handler = ui_manager.handle_main_menu_input_keyboard(event, self.menu_selected_option)
                if new_selection_key != self.menu_selected_option:
                    self.menu_selected_option = new_selection_key
                if key_action_from_handler: key_action = key_action_from_handler
                
                if event.type == pygame.MOUSEMOTION:
                    if hasattr(self, 'menu_option_rects') and self.menu_option_rects: 
                        for i, rect in enumerate(self.menu_option_rects):
                            if rect.collidepoint(current_event_logical_mouse_pos): 
                                if self.menu_selected_option != i: self.menu_selected_option = i
                                break 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        if hasattr(self, 'menu_option_rects') and self.menu_option_rects:
                            for i, rect in enumerate(self.menu_option_rects):
                                if rect.collidepoint(current_event_logical_mouse_pos): 
                                    self.menu_selected_option = i 
                                    if i == 0: mouse_click_action = "vs_bot"
                                    elif i == 1: mouse_click_action = "pvp"
                                    elif i == 2: mouse_click_action = "toggle_fullscreen"
                                    break
            
            elif self.current_state in [STATE_NAME_INPUT_P1_BOT, STATE_NAME_INPUT_P1_PVP, STATE_NAME_INPUT_P2_PVP]:
                self.name_input_text, confirmed = ui_manager.handle_name_input_text(event, self.name_input_text)
                if confirmed:
                    if self.current_state == STATE_NAME_INPUT_P1_BOT:
                        self.player1.name = self.name_input_text if self.name_input_text.strip() else "Гравець"
                        self.start_new_game_session()
                    elif self.current_state == STATE_NAME_INPUT_P1_PVP:
                        self.player1.name = self.name_input_text if self.name_input_text.strip() else "Гравець 1"
                        self.change_state(STATE_NAME_INPUT_P2_PVP)
                    elif self.current_state == STATE_NAME_INPUT_P2_PVP:
                        self.player2.name = self.name_input_text if self.name_input_text.strip() else "Гравець 2"
                        self.start_new_game_session()
            
            elif self.current_state == STATE_GAMEPLAY:
                if not self.game_active and self.winner: 
                    game_over_action = ui_manager.handle_game_over_input(event)
                    if game_over_action == "replay": self.start_new_game_session()
                    elif game_over_action == "main_menu": self.change_state(STATE_MAIN_MENU)
                    elif game_over_action == "quit": self.is_running = False
        
        final_action = key_action or mouse_click_action
        if self.current_state == STATE_MAIN_MENU and final_action:
            print(f"DEBUG: Отримано фінальну дію з меню: '{final_action}'")
            if final_action == "vs_bot":
                self.play_against_bot = True; self.player2.name = "Русланчик" 
                self.change_state(STATE_NAME_INPUT_P1_BOT)
            elif final_action == "pvp":
                self.play_against_bot = False; self.change_state(STATE_NAME_INPUT_P1_PVP)
            elif final_action == "toggle_fullscreen": self.toggle_fullscreen()
            elif final_action == "quit": self.is_running = False

        if self.current_state == STATE_GAMEPLAY and self.game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: self.player1.move_up()
            if keys[pygame.K_s]: self.player1.move_down() 
            if not self.play_against_bot:
                if keys[pygame.K_UP]: self.player2.move_up()
                if keys[pygame.K_DOWN]: self.player2.move_down()


    def _update_logic(self):
        if self.current_state == STATE_GAMEPLAY and self.game_active:
            self.ball.move()
            if self.play_against_bot:
                bot.control_bot_paddle(self.player2, self.ball) 
            self._process_collisions()
            self._process_scoring()

    def _process_collisions(self):
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= LOGICAL_HEIGHT:
            self.ball.bounce('y')

        paddles = [self.player1, self.player2]
        for i, paddle in enumerate(paddles):
            if self.ball.rect.colliderect(paddle.rect):
                moving_towards_p1 = self.ball.velocity_x < 0 and i == 0
                moving_towards_p2 = self.ball.velocity_x > 0 and i == 1

                if moving_towards_p1 or moving_towards_p2:
                    if moving_towards_p1 and self.ball.rect.left <= paddle.rect.right:
                         self.ball.rect.left = paddle.rect.right + 1 
                    elif moving_towards_p2 and self.ball.rect.right >= paddle.rect.left:
                         self.ball.rect.right = paddle.rect.left -1 
                    
                    hit_pos_ratio = (paddle.rect.centery - self.ball.rect.centery) / (PADDLE_HEIGHT / 2)
                    hit_pos_ratio = max(-1, min(1, hit_pos_ratio)) 
                    self.ball.bounce('x', -hit_pos_ratio) 
                    break 

    def _process_scoring(self):
        if self.ball.rect.left <= 0: 
            self.score2 += 1
            self.ball.reset() 
            if self.score2 >= WINNING_SCORE:
                self.winner = self.player2.name; self.game_active = False
        elif self.ball.rect.right >= LOGICAL_WIDTH: 
            self.score1 += 1
            self.ball.reset()
            if self.score1 >= WINNING_SCORE:
                self.winner = self.player1.name; self.game_active = False
                
    def _render_gameplay(self):
        self.logical_surface.fill(BG_COLOR) 
        self.player1.draw(self.logical_surface)
        self.player2.draw(self.logical_surface)
        self.ball.draw(self.logical_surface)
        pygame.draw.aaline(self.logical_surface, LIGHT_GREY, 
                           (LOGICAL_WIDTH / 2, 0), 
                           (LOGICAL_WIDTH / 2, LOGICAL_HEIGHT))

        ui_manager.draw_text(self.logical_surface, str(self.score1), self.assets.score_font, LIGHT_GREY, 
                             LOGICAL_WIDTH / 4, 50)
        ui_manager.draw_text(self.logical_surface, str(self.score2), self.assets.score_font, LIGHT_GREY, 
                             LOGICAL_WIDTH * 3 / 4, 50)
        
        ui_manager.draw_text(self.logical_surface, self.player1.name, self.assets.small_message_font, LIGHT_GREY,
                             LOGICAL_WIDTH / 4, 90)
        ui_manager.draw_text(self.logical_surface, self.player2.name, self.assets.small_message_font, LIGHT_GREY,
                             LOGICAL_WIDTH * 3 / 4, 90)

        if not self.game_active and self.winner:
            ui_manager.display_game_over_message(self.logical_surface, self.assets, self.winner)


    def _render(self):
        self.logical_surface.fill(BG_COLOR) 

        if self.current_state == STATE_MAIN_MENU:
            self.menu_option_rects = ui_manager.display_main_menu(self.logical_surface, self.assets, 
                                                                  self.menu_selected_option, 
                                                                  self.is_fullscreen) 
        
        elif self.current_state == STATE_NAME_INPUT_P1_BOT:
            ui_manager.display_name_input(self.logical_surface, self.assets, 
                                          f"Введіть ім'я, {self.player1.name}:", 
                                          self.name_input_text, self.name_input_active)
        elif self.current_state == STATE_NAME_INPUT_P1_PVP:
             ui_manager.display_name_input(self.logical_surface, self.assets, 
                                          f"Введіть ім'я, {self.player1.name}:", 
                                          self.name_input_text, self.name_input_active)
        elif self.current_state == STATE_NAME_INPUT_P2_PVP:
             ui_manager.display_name_input(self.logical_surface, self.assets, 
                                          f"Введіть ім'я, {self.player2.name}:", 
                                          self.name_input_text, self.name_input_active)
        
        elif self.current_state == STATE_GAMEPLAY:
            self._render_gameplay() 
            
        self.screen.fill(BLACK) 
        self._calculate_scale_and_offsets() 
        
        scaled_surface_to_blit = pygame.transform.smoothscale(self.logical_surface, (self.scaled_width, self.scaled_height))
        self.screen.blit(scaled_surface_to_blit, (self.offset_x, self.offset_y))
        
        pygame.display.flip()

    def change_state(self, new_state):
        if self.current_state == new_state and new_state == STATE_MAIN_MENU:
             pass
        else:
            print(f"Зміна стану з {self.current_state} на {new_state}") 
            self.current_state = new_state
            self.name_input_text = "" 
            self.name_input_active = True 

        if new_state == STATE_MAIN_MENU:
            self.game_active = False 
            self.winner = None
        elif new_state == STATE_NAME_INPUT_P1_BOT:
            self.player1.name = "Гравець" 
        elif new_state == STATE_NAME_INPUT_P1_PVP:
            self.player1.name = "Гравець 1"
        elif new_state == STATE_NAME_INPUT_P2_PVP:
            self.player2.name = "Гравець 2"

    def start_new_game_session(self):
        self.score1 = 0; self.score2 = 0
        self.winner = None
        self.ball.reset() 
        self.player1.reset_position()
        self.player2.reset_position()
        
        self.change_state(STATE_GAMEPLAY)
        self.game_active = True


    def run_game_loop(self):
        while self.is_running:
            self._process_input()
            if not self.is_running: break
            self._update_logic()
            self._render()
            self.clock.tick(60)