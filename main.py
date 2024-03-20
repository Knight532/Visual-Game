import os
import random
import pygame
from pygame.constants import QUIT, K_LEFT, K_RIGHT, K_UP

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200


FONT = pygame.font.SysFont('Verdana', 20)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Завантаження зображення гравця
PLAYER_IMAGE_LEFT = "D:\\Dev\Projects\\Visual Game\\animation_player\\player_left"
PLAYER_IMAGE_RIGHT = "D:\\Dev\Projects\\Visual Game\\animation_player\\player_right"
PLAYER_IMAGES_LEFT = os.listdir(PLAYER_IMAGE_LEFT)
PLAYER_IMAGES_RIGHT = os.listdir(PLAYER_IMAGE_RIGHT)
CHANGE_IMAGE = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_IMAGE, 200)

# Завантаження зображення ворога
ENEMY_IMAGE_LEFT = "D:\\Dev\Projects\\Visual Game\\animation_enemy\\enemy_left"
ENEMY_IMAGE_RIGHT = "D:\\Dev\Projects\\Visual Game\\animation_enemy\\enemy_right"
ENEMY_IMAGES_LEFT = os.listdir(ENEMY_IMAGE_LEFT)
ENEMY_IMAGES_RIGHT = os.listdir(ENEMY_IMAGE_RIGHT)
ENEMY_CHANGE_IMAGE = pygame.USEREVENT + 2
pygame.time.set_timer(ENEMY_CHANGE_IMAGE, 200)

# Створення гравця
player_size = (91, 161)
player_image = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\player.png').convert_alpha(), player_size)
player_rect = player_image.get_rect()
player_move_up = [0, -6]  # Збільшимо значення швидкості при стрибку
player_move_left = [-2, 0]
player_move_right = [2, 0]
player_health = 100
player_attack = random.randint(5, 20)

#Створення ворога
enemy_size = (91, 161)
enemy_image = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\enemy.png').convert_alpha(), player_size)
enemy_rect = enemy_image.get_rect()
enemy_speed = 2
enemy_health = 100
enemy_attack = random.randint(5, 20)

player_rect.centerx = WIDTH // 5.5  # По горизонталі в центрі
player_rect.bottom = HEIGHT // 1.25
background_image = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\background.png').convert_alpha(), (WIDTH, HEIGHT))

# Початкове положення ворога
enemy_rect.centerx = WIDTH // 1.2  # По горизонталі в правому куті
enemy_rect.bottom = HEIGHT // 1.25

player_x = player_rect.centerx
enemy_x = enemy_rect.centerx

animate_enemy = True
enemy_image_index = 0

timer_font = pygame.font.SysFont('Verdana', 40)
timer_color = (0, 255, 0)
start_ticks = pygame.time.get_ticks()  # Отримання часу початку

playing = True
is_jumping = False
animate_player = False
jump_count = 10  # Кількість кадрів, протягом яких гравець пригатиме
image_index = 0

def draw_health_bar_player(surface, health):
    # Визначення параметрів полоски здоров'я
    bar_length = 200
    bar_height = 20
    health_bar = pygame.Rect(100, 20, bar_length, bar_height)
    
    # Здоров'я гравця відображається червоною полоскою
    pygame.draw.rect(surface, (255, 0, 0), health_bar)
    
    # Обмеження, щоб полоска здоров'я не могла бути меншою за 0
    current_health = max(health, 0)
    
    # Визначення ширини полоски здоров'я відповідно до поточного здоров'я
    bar_width = int(bar_length * current_health / 100)
    health_bar.width = bar_width
    
    # Малювання полоски здоров'я залежно від поточного здоров'я
    pygame.draw.rect(surface, (0, 255, 0), health_bar)

def draw_health_bar_enemy(surface, health):
    # Визначення параметрів полоски здоров'я
    bar_length = 200
    bar_height = 20
    health_bar = pygame.Rect(WIDTH - bar_length - 100, 20, bar_length, bar_height)  # Змінюємо координати для правого верхнього кута

    # Здоров'я ворога відображається червоною полоскою
    pygame.draw.rect(surface, (255, 0, 0), health_bar)

    # Обмеження, щоб полоска здоров'я не могла бути меншою за 0
    current_health = max(health, 0)

    # Визначення ширини полоски здоров'я відповідно до поточного здоров'я
    bar_width = int(bar_length * current_health / 100)
    health_bar.width = bar_width

    # Малювання полоски здоров'я залежно від поточного здоров'я
    pygame.draw.rect(surface, (0, 255, 0), health_bar)
    
def frame_player():
    frame_size = (50, 50)
    frame_position = (20, 10)

    # Намалювати рамку на екрані
    frame_rect = pygame.Rect(frame_position, frame_size)
    pygame.draw.rect(main_display, (255, 255, 255), frame_rect, 2)  # Рамка буде білого кольору та товщиною 2 пікселя

    # Відобразіть зображення гравця всередині рамки
    player_image_scaled = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\player_img.png').convert_alpha(), (frame_size[0]-10, frame_size[1]-10))  # Зменшити розмір зображення гравця на 10 пікселів від кожного боку
    player_rect_frame = player_image_scaled.get_rect(center=frame_rect.center)
    return player_image_scaled, player_rect_frame

def frame_enemy():
    frame_size = (50, 50)
    frame_position = (1125, 10)

    # Намалювати рамку на екрані
    frame_rect = pygame.Rect(frame_position, frame_size)
    pygame.draw.rect(main_display, (255, 255, 255), frame_rect, 2)  # Рамка буде білого кольору та товщиною 2 пікселя

    # Відобразіть зображення гравця всередині рамки
    player_image_scaled = pygame.transform.scale(pygame.image.load('D:\\Dev\\Projects\\Visual Game\\enemy_img.png').convert_alpha(), (frame_size[0]-10, frame_size[1]-10))  # Зменшити розмір зображення гравця на 10 пікселів від кожного боку
    player_rect_frame = player_image_scaled.get_rect(center=frame_rect.center)
    return player_image_scaled, player_rect_frame

while playing:
    FPS.tick(120)
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Кількість секунд з початку
    
    # Перевірка на перемогу
    if seconds >= 90:  # Якщо пройшло 90 секунд, гра завершується
        playing = False
        winner = "Player" if player_health < enemy_health else "Enemy"
        print(f"The winner is {winner}!")

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_UP and not is_jumping:  
                is_jumping = True
                jump_count = 30  # Встановлюємо кількість кадрів стрибка

        if event.type == CHANGE_IMAGE:
            if animate_player:  # Перевіряємо, чи потрібно змінювати зображення гравця
                player_image = pygame.image.load(os.path.join(PLAYER_IMAGE_RIGHT, PLAYER_IMAGES_RIGHT[image_index]))
                player_image = pygame.transform.scale(player_image, player_size)  # Змінюємо розмір зображення
                image_index += 1
                if image_index >= len(PLAYER_IMAGES_RIGHT):
                    image_index = 0

        if event.type == ENEMY_CHANGE_IMAGE:
            if animate_enemy:  # Перевіряємо, чи потрібно змінювати зображення ворога
                enemy_image = pygame.image.load(os.path.join(ENEMY_IMAGE_LEFT, ENEMY_IMAGES_LEFT[enemy_image_index]))
                enemy_image = pygame.transform.scale(enemy_image, enemy_size)  # Змінюємо розмір зображення
                enemy_image_index += 1
                if enemy_image_index >= len(ENEMY_IMAGES_LEFT):
                    enemy_image_index = 0

    keys = pygame.key.get_pressed()

    # Обробка руху гравця
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(-3, 0)  # Рух вліво
        animate_player = True  # Встановлюємо прапорець анімації

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(3, 0)  # Рух вправо
        animate_player = True  # Встановлюємо прапорець анімації

        

    if enemy_rect.left <= 0 or enemy_rect.right >= WIDTH:
        enemy_speed *= -1  # Змінюємо напрям руху, якщо ворог досяг краю екрану

    enemy_rect = enemy_rect.move(enemy_speed, 0)  # Рух ворога

    # AI для атаки гравця
    if player_rect.colliderect(enemy_rect):
        # Якщо гравець і ворог зіштовхнулися, ворог атакує гравця
        player_health -= enemy_attack

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

    #Відображення ворога
    main_display.blit(enemy_image, enemy_rect)

    if 80 <= seconds <= 90:  # Час 80-90 секунд (останні 10 секунд)
        timer_color = (255, 0, 0)  # Червоний колір
    else:
        timer_color = (0, 255, 0)  # Зелений колір

    timer_text = timer_font.render(f"{90 - seconds}", True, timer_color)
    main_display.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))
    player_image_scaled, player_rect_frame = frame_player()
    main_display.blit(player_image_scaled, player_rect_frame)
    enemy_image_scaled, enemy_rect_frame = frame_enemy()
    main_display.blit(enemy_image_scaled, enemy_rect_frame)
    

    draw_health_bar_player(main_display, player_health)
    draw_health_bar_enemy(main_display, enemy_health)


    pygame.display.flip()