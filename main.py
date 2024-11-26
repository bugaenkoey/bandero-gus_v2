import random
from os import listdir
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, K_RETURN, K_SPACE

# Ініціалізація Pygame
pygame.init()
FPS = pygame.time.Clock()

# Визначення кольорів
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Шрифт для відображення очок
FONT = pygame.font.SysFont(None, 32)

# Розміри вікна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Створення поверхні для відображення
main_surface = pygame.display.set_mode(SCREEN_SIZE)

# Шлях до зображень гравця
IMGS_PATH = 'goose'
player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_imgs[0]  # Встановлюємо перше зображення як початкове
player_rect = player.get_rect()
player_speed = 5

def create_enemy():
    """Функція створення ворогів з їх властивостями."""
    enemy_img = pygame.image.load('enemy.png').convert_alpha()
    enemy_speed = random.randint(2, 5)
    enemy_size = (enemy_speed * 20, int(enemy_speed * 6.6))
    enemy = pygame.transform.scale(enemy_img, enemy_size)
    enemy_rect = pygame.Rect(SCREEN_WIDTH - 50, random.randint(200, SCREEN_HEIGHT - 200), *enemy.get_size())
    return [enemy, enemy_rect, enemy_speed, enemy.get_size(), enemy_img]

def create_bonus():
    """Функція створення бонусів з їх властивостями."""
    bonus_img = pygame.image.load('bonus.png').convert_alpha()
    bonus_speed = random.randint(1, 3)
    bonus_size = (bonus_speed * 70, bonus_speed * 70)
    bonus = pygame.transform.scale(bonus_img, bonus_size)
    bonus_rect = pygame.Rect(random.randint(200, SCREEN_WIDTH - 200), 0, *bonus.get_size())
    return [bonus, bonus_rect, bonus_speed, bonus.get_size(), bonus_img]

def shaker(items):
    """Функція для випадкової зміни розміру елементів."""
    for item in items:
        item_rnd = random.randint(item[2], item[2] * 5)
        item[0] = pygame.transform.scale(item[4], (item[3][0] - item_rnd, item[3][1] + item_rnd))

# Завантаження фону
bg = pygame.transform.scale(pygame.image.load('background.png').convert(), SCREEN_SIZE)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

# Події для створення ворогів, бонусів, зміни зображення та тряски
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1000)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 150)

SHAKE = pygame.USEREVENT + 4
pygame.time.set_timer(SHAKE, 50)

# Списки для ворогів і бонусів
enemies = []
bonuses = []

scores = 0
img_index = 0
is_working = True
game_over = False
quit_game = False

def reset_game():
    """Функція для скидання гри."""
    global enemies, bonuses, scores, img_index, is_working, game_over, player_rect
    enemies = []
    bonuses = []
    scores = 0
    img_index = 0
    is_working = True
    game_over = False
    player_rect.topleft = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_rect.height)

def display_message(message, sub_message):
    """Функція для відображення повідомлень на екрані."""
    main_surface.fill(BLACK)
    main_message = FONT.render(message, True, RED)
    sub_message = FONT.render(sub_message, True, RED)
    main_surface.blit(main_message, (SCREEN_WIDTH // 2 - main_message.get_width() // 2, SCREEN_HEIGHT // 2 - main_message.get_height() // 2))
    main_surface.blit(sub_message, (SCREEN_WIDTH // 2 - sub_message.get_width() // 2, SCREEN_HEIGHT // 2 + main_message.get_height() // 2))
    pygame.display.flip()

def handle_events():
    """Функція для обробки подій."""
    global is_working, game_over, quit_game,player
    for event in pygame.event.get():
        if event.type == QUIT or pygame.key.get_pressed()[K_ESCAPE]:
            # quit_game = True
            is_working = False
            return False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            global img_index
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]
            # player_imgs[img_index]

        if event.type == SHAKE:
            shaker(enemies)
            shaker(bonuses)

        if event.type == pygame.KEYDOWN and event.key == K_RETURN and game_over:
            reset_game()

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            player_rect.centerx = mouse_x
            player_rect.centery = mouse_y

    return True

# Головний ігровий цикл
while not quit_game:
    while is_working:
        FPS.tick(60)

        handle_events()

        if not game_over:
            bgX -= bg_speed
            bgX2 -= bg_speed

            if bgX < -bg.get_width():
                bgX = bg.get_width()

            if bgX2 < -bg.get_width():
                bgX2 = bg.get_width()

            main_surface.blit(bg, (bgX, 0))
            main_surface.blit(bg, (bgX2, 0))

            main_surface.blit(player, player_rect)
            main_surface.blit(FONT.render(str(scores), True, RED), (0, 0))

            for enemy in enemies:
                enemy[1] = enemy[1].move(-enemy[2], 0)
                main_surface.blit(enemy[0], enemy[1])

                if enemy[1].left < 2 - enemy[3][0]:
                    enemies.pop(enemies.index(enemy))

                if player_rect.colliderect(enemy[1]):
                    enemies.pop(enemies.index(enemy))
                    scores -= 1

            for bonus in bonuses:
                bonus[1] = bonus[1].move(0, bonus[2])
                main_surface.blit(bonus[0], bonus[1])

                if bonus[1].bottom > SCREEN_HEIGHT + bonus[3][0]:
                    game_over = True
                    display_message("Game Over", "Press Enter to Restart or Esc to Quit")
                    break

                if player_rect.colliderect(bonus[1]):
                    bonuses.pop(bonuses.index(bonus))
                    scores += 1

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
                player_rect = player_rect.move(0, player_speed)
            if pressed_keys[K_UP] and player_rect.top > 0:
                player_rect = player_rect.move(0, -player_speed)
            if pressed_keys[K_RIGHT] and player_rect.right < SCREEN_WIDTH:
                player_rect = player_rect.move(player_speed, 0)
            if pressed_keys[K_LEFT] and player_rect.left > 0:
                player_rect = player_rect.move(-player_speed, 0)

        pygame.display.flip()

    if game_over:
        display_message("Game Over", "Press Enter to Restart or Esc to Quit")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    reset_game()
                elif event.key == K_ESCAPE:
                    is_working = False
                    quit_game = True
        break

    if not quit_game:
        display_message("Press Enter to continue game", "or Esc to exit")
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    is_working = True
                    game_over = False
                elif event.key == K_ESCAPE:
                    quit_game = True
            break
