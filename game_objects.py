# game_objects.py
import pygame
import random
# Змінено SCREEN_HEIGHT на LOGICAL_HEIGHT
from constants import PADDLE_HEIGHT, LOGICAL_HEIGHT, BALL_SPEED_INCREASE_FACTOR, MAX_BALL_SPEED_FACTOR, PADDLE_SPEED 
# Додав PADDLE_SPEED, якщо він потрібен для логіки бота (хоча зараз він береться з self.speed)

class Paddle:
    def __init__(self, x, y, width, height, color, speed, name="Гравець"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed
        self.name = name
        self.initial_x = x
        self.initial_y = y

    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self): # Використовуємо LOGICAL_HEIGHT з constants
        self.rect.y += self.speed
        if self.rect.bottom > LOGICAL_HEIGHT: # Змінено на LOGICAL_HEIGHT
            self.rect.bottom = LOGICAL_HEIGHT

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def reset_position(self):
        self.rect.x = self.initial_x
        # Центруємо ракетку по вертикалі відносно LOGICAL_HEIGHT
        self.rect.y = LOGICAL_HEIGHT / 2 - PADDLE_HEIGHT / 2 
        # Або повертаємо на self.initial_y, якщо це більш коректно для логіки
        # self.rect.y = self.initial_y # Якщо initial_y вже розраховано правильно

class Ball:
    def __init__(self, x, y, radius, color, base_speed_x, base_speed_y):
        self.radius = radius
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = color
        
        self.base_speed_x = abs(base_speed_x)
        self.base_speed_y = abs(base_speed_y)
        
        # Зберігаємо початковий центр відносно логічних розмірів
        self.initial_center_x = x 
        self.initial_center_y = y
        
        self.velocity_x = self.base_speed_x * random.choice((1, -1))
        self.velocity_y = self.base_speed_y * random.choice((1, -1))

    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

    def bounce(self, axis, paddle_hit_pos_ratio=0):
        if axis == 'y':
            self.velocity_y *= -1
        elif axis == 'x':
            self.velocity_x *= -1
            self.velocity_x *= BALL_SPEED_INCREASE_FACTOR
            self.velocity_y += paddle_hit_pos_ratio * self.base_speed_y * 0.5 
            self.velocity_y *= BALL_SPEED_INCREASE_FACTOR

            max_vx = self.base_speed_x * MAX_BALL_SPEED_FACTOR
            max_vy = self.base_speed_y * MAX_BALL_SPEED_FACTOR

            if abs(self.velocity_x) > max_vx:
                self.velocity_x = max_vx if self.velocity_x > 0 else -max_vx
            if abs(self.velocity_y) > max_vy:
                self.velocity_y = max_vy if self.velocity_y > 0 else -max_vy

    def reset(self): # Тепер не приймає аргументів, використовує збережені initial_center
        self.rect.center = (self.initial_center_x, self.initial_center_y)
        self.velocity_x = self.base_speed_x * random.choice((1, -1))
        self.velocity_y = self.base_speed_y * random.choice((1, -1))