import os
import pygame
import random
from pygame.constants import QUIT, K_LEFT, K_RIGHT, K_UP

pygame.init()

class Player():
    def __init__(self):
        health = 100

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Завантаження зображення гравця
player_size = (91, 161)
player_image = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\player.png').convert_alpha(), player_size)
player_rect = player_image.get_rect()
player_move_up = [0, -6]  # Збільшимо значення швидкості при стрибку
player_move_left = [-3, 0]
player_move_right = [3, 0]

player_rect.centerx = WIDTH // 5.5  # По горизонталі в центрі
player_rect.bottom = HEIGHT // 1.25
background_image = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\background.png').convert_alpha(), (WIDTH, HEIGHT))

playing = True
is_jumping = False
jump_count = 10  # Кількість кадрів, протягом яких гравець пригаватиме

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:  # Перевіряємо натискання клавіші
            if event.key == pygame.K_UP and not is_jumping:  # Якщо натиснута клавіша вгору і гравець не стрибає вже
                is_jumping = True
                jump_count = 30  # Встановлюємо кількість кадрів стрибка

    keys = pygame.key.get_pressed()

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    # Обробка стрибка
    if is_jumping:
        if jump_count >= -30:  # Зупиняємо стрибок після певної кількості кадрів
            player_rect.y -= (jump_count * abs(jump_count)) * 0.03  # Формула для анімації при стрибку
            jump_count -= 1
        else:
            jump_count = 30
            is_jumping = False

    # Відображення фону
    main_display.blit(background_image, (0, 0))
    
    # Відображення гравця
    main_display.blit(player_image, player_rect)

    pygame.display.flip()