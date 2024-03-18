import os
import pygame
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
IMAGE_PATH = "animation_player"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
CHANGE_IMAGE = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_IMAGE, 200)

player_size = (91, 161)
player_image = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\player.png').convert_alpha(), player_size)
player_rect = player_image.get_rect()
player_move_up = [0, -6]  # Збільшимо значення швидкості при стрибку
player_move_left = [-2, 0]
player_move_right = [2, 0]

player_rect.centerx = WIDTH // 5.5  # По горизонталі в центрі
player_rect.bottom = HEIGHT // 1.25
background_image = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\background.png').convert_alpha(), (WIDTH, HEIGHT))

playing = True
is_jumping = False
animate_player = False
jump_count = 10  # Кількість кадрів, протягом яких гравець пригаватиме
image_index = 0

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_UP and not is_jumping:  
                is_jumping = True
                jump_count = 30  # Встановлюємо кількість кадрів стрибка

        if event.type == CHANGE_IMAGE:
            if animate_player:  # Перевіряємо, чи потрібно змінювати зображення гравця
                player_image = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                player_image = pygame.transform.scale(player_image, player_size)  # Змінюємо розмір зображення
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0

    keys = pygame.key.get_pressed()

    # Обробка руху гравця
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(-3, 0)  # Рух вліво
        animate_player = True  # Встановлюємо прапорець анімації

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(3, 0)  # Рух вправо
        animate_player = True  # Встановлюємо прапорець анімації

    # Якщо гравець не рухається, встановлюємо прапорець анімації в False
    if not keys[K_LEFT] and not keys[K_RIGHT]:
        animate_player = False

    # Обробка стрибка
    if is_jumping:
        if jump_count >= -30:  
            player_rect.y -= (jump_count * abs(jump_count)) * 0.03  
            jump_count -= 1
        else:
            jump_count = 30
            is_jumping = False

    # Відображення фону
    main_display.blit(background_image, (0, 0))
    
    # Відображення гравця
    main_display.blit(player_image, player_rect)

    pygame.display.flip()