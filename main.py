import random
import pygame
import os
import sqlite3
from pygame_widgets import Button, Slider
from src.player import Player
from src.camera import Camera
from src.obstacle import Obstacle
from src.gem import Gem
from src.explosion import Explosion
from src.sparkle import Sparkle


def menu_to_running():
    global menu
    global running
    menu = False
    running = True
    restart()


def running_to_menu():
    global menu
    global running
    global running_pause
    global profile
    menu = True
    running = False
    running_pause = False
    profile = False


def unpause():
    global running_pause
    running_pause = False


def restart():
    global player
    global obstacles
    global running_pause
    global camera
    global gems
    global sparkles
    global explosions
    global score
    score = 0
    sparkles = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    player = Player()
    camera = Camera()
    obstacles = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    running_pause = False


def volume():  # функция для изменения звука(вызывется в главном цикле)
    pygame.mixer.Sound.set_volume(soundtrack, volume_slider.getValue() / 100)


def pick_profile():
    global profile
    global menu
    profile = True
    menu = False


def pick_p(name, value):
    global profile
    global menu
    global menu_b_profiles
    global moneys
    profile = False
    menu = True
    menu_b_profiles = Button(screen, 0, 0, 200, 40, text=name,
                             fontSize=40, hoverColour=(78, 163, 39),
                             inactiveColour=(50, 122, 17),
                             pressedColour=(231, 247, 49),
                             textColour=(0, 0, 255),
                             onClick=pick_profile)
    moneys = font.render(f'{value}', False, (100, 255, 100))


pygame.init()
pygame.mixer.init()
con = sqlite3.connect(os.path.join('src\\profiles.db'))
cur = con.cursor()
font = pygame.font.Font(None, 120)
soundtrack = pygame.mixer.Sound(os.path.join(
    'images\\imperial_march.wav'))  # путь до музыки в меню
money_image = pygame.image.load(os.path.join(
    'images\\Space\\gems\\money.png'))  # иконка валюты в меню
volume_image = pygame.image.load(os.path.join(
    'images\\volume_icon.png'))  # иконка звука в меню
volume_image = pygame.transform.scale(volume_image, (75, 75))
money_image = pygame.transform.scale(money_image, (75, 75))
moneys = font.render("0", False, (100, 255, 100))
pygame.mixer.Sound.play(soundtrack)
pygame.mixer.Sound.set_volume(soundtrack, 0.4)
result = cur.execute("""SELECT * FROM data""").fetchall()
fps = 60
obs_count = 0
nifo = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 960))
pause_b = pygame.Surface((750, 600))
pause = pygame.Surface((750, 600))
profiles = pygame.Surface((750, 800))
profiles_b = pygame.Surface((750, 800))
pygame.mouse.set_visible(False)
# слайдер, можно дизайн переделать
volume_slider = Slider(screen, 100, 920, 200, 20, min=0, max=100, step=10)
menu_b_profiles = Button(screen, 0, 0, 200, 40, text='Профили',
                         fontSize=40, hoverColour=(78, 163, 39),
                         inactiveColour=(50, 122, 17),
                         pressedColour=(231, 247, 49),
                         textColour=(0, 0, 255),
                         onClick=pick_profile)
menu_b_start = Button(screen, 440, 200, 400, 70, text='Играть',
                      fontSize=40, hoverColour=(78, 163, 39),
                      inactiveColour=(50, 122, 17),
                      pressedColour=(231, 247, 49), radius=20,
                      textColour=(0, 0, 255),
                      onClick=menu_to_running)
menu_b_hangar = Button(screen, 440, 350, 400, 70, text='Ангар',
                       fontSize=40, hoverColour=(78, 163, 39),
                       inactiveColour=(50, 122, 17),
                       pressedColour=(231, 247, 49), radius=20,
                       textColour=(0, 0, 255),
                       onClick=lambda: print('Click'))
menu_b_top = Button(screen, 440, 500, 400, 70, text='Таблица рекордов',
                    fontSize=40, hoverColour=(78, 163, 39),
                    inactiveColour=(50, 122, 17),
                    pressedColour=(231, 247, 49), radius=20,
                    textColour=(0, 0, 255),
                    onClick=lambda: print('Click'))
menu_b_quit = Button(screen, 440, 650, 400, 70, text='Выйти из игры',
                     fontSize=40, hoverColour=(78, 163, 39),
                     inactiveColour=(50, 122, 17),
                     pressedColour=(231, 247, 49), radius=20,
                     textColour=(0, 0, 255),
                     onClick=lambda: pygame.quit())
pause_b_coninue = Button(pause_b, 50, 360, 300, 60, text='Продолжить',
                         fontSize=40, hoverColour=(78, 163, 39),
                         inactiveColour=(50, 122, 17),
                         pressedColour=(231, 247, 49), radius=20,
                         textColour=(0, 0, 255),
                         onClick=lambda: unpause())
pause_b_restart = Button(pause_b, 50, 500, 300, 60, text='Заново',
                         fontSize=40, hoverColour=(78, 163, 39),
                         inactiveColour=(50, 122, 17),
                         pressedColour=(231, 247, 49), radius=20,
                         textColour=(0, 0, 255),
                         onClick=lambda: restart())
pause_b_menu = Button(pause_b, 400, 360, 300, 60, text='В главное меню',
                      fontSize=40, hoverColour=(78, 163, 39),
                      inactiveColour=(50, 122, 17),
                      pressedColour=(231, 247, 49), radius=20,
                      textColour=(0, 0, 255),
                      onClick=lambda: running_to_menu())
pause_b_quit = Button(pause_b, 400, 500, 300, 60, text='Выйти из игры',
                      fontSize=40, hoverColour=(78, 163, 39),
                      inactiveColour=(50, 122, 17),
                      pressedColour=(231, 247, 49), radius=20,
                      textColour=(0, 0, 255),
                      onClick=lambda: pygame.quit())
profile_1 = Button(profiles_b, 225, 100, 295, 55, text=f'{result[0][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=lambda: pick_p(result[0][1], result[0][2]))
profile_2 = Button(profiles_b, 225, 250, 295, 55, text=f'{result[1][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=lambda: pick_p(result[1][1], result[1][2]))
profile_3 = Button(profiles_b, 225, 400, 295, 55, text=f'{result[2][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=lambda: pick_p(result[2][1], result[2][2]))
profile_4 = Button(profiles_b, 225, 550, 295, 55, text=f'{result[3][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=lambda: pick_p(result[3][1], result[3][2]))
menu_prof = Button(profiles_b, 210, 700, 335, 55, text='Вернуться в меню',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=lambda: running_to_menu())
running = False
running_pause = False
profile = False
menu = True
cursor = pygame.image.load(os.path.join('images\\arrow.png')).convert_alpha()
while True:
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                con.close()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_pause = True
                if not running_pause:
                    if event.key == pygame.K_LEFT:
                        player.direction = 5
                    if event.key == pygame.K_RIGHT:
                        player.direction = -5
            if event.type == pygame.KEYUP:
                if not running_pause:
                    if event.key == pygame.K_LEFT:
                        player.direction = 0
                    if event.key == pygame.K_RIGHT:
                        player.direction = 0
        bg_running = pygame.transform.scale(pygame.image.load(os.path.join(
            'images\\Backgrounds\\space.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_running, (0, 0))
        if not running_pause:
            camera.apply(player)
        if not player.is_game_over:
            screen.blit(player.image, (player.rect.x, player.rect.y))
        for sprite in enumerate(obstacles):
            if not running_pause:
                camera.apply(sprite[1])
                if sprite[1].update(obstacles):  # Взрыв
                    explosion = Explosion()
                    explosion.rect.x = sprite[1].rect.x
                    explosion.rect.y = sprite[1].rect.y
                    explosions.add(explosion)
            screen.blit(sprite[1].image, (sprite[1].rect.x, sprite[1].rect.y))
            if obs_count == 60:
                if sprite[0] == 1 + nifo:
                    if not (-660 < sprite[1].rect.x < 1640 and -660 < sprite[1].rect.y < 1640):
                        sprite[1].kill()
                        obs_count -= 1
                        nifo = 0
                    else:
                        nifo += 1
            if pygame.sprite.collide_mask(player, sprite[1]):  # Взрыв
                sprite[1].kill()
                player.is_game_over = True
                explosion = Explosion()
                explosion.rect.x = player.rect.x
                explosion.rect.y = player.rect.y
                explosions.add(explosion)
        for sprite in gems:
            if (sprite.rect.x > 2640 or sprite.rect.x < -1360) and (sprite.rect.y > 2640 or sprite.rect.y < -1360):
                sprite.kill()
            if not running_pause:
                camera.apply(sprite)
            if pygame.sprite.collide_mask(player, sprite):  #  Гем
                sprite.kill()
                sparkle = Sparkle()
                sparkle.rect.x = player.rect.x
                sparkle.rect.y = player.rect.y
                sparkles.add(sparkle)
            screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
            sprite.update()
        for sprite in explosions:
            if not running_pause:
                sprite.update()
            screen.blit(sprite.explosion, (sprite.rect.x, sprite.rect.y))
            camera.apply(sprite)
        for sprite in sparkles:
            if not running_pause:
                sprite.update()
            screen.blit(sprite.sparkle, (sprite.rect.x, sprite.rect.y))
            camera.apply(sprite)
        screen.blit(money_image, (1200, 5))
        if running_pause:
            pause.fill((0, 80, 199))
            pause.set_alpha(75)
            screen.blit(pause, (240, 100))
            pause_b.set_colorkey('BLACK')
            screen.blit(pause_b, (240, 100))
            pause_b_coninue.listen(events)
            pause_b_coninue.draw()
            pause_b_restart.listen(events)
            pause_b_restart.draw()
            pause_b_menu.listen(events)
            pause_b_menu.draw()
            pause_b_quit.listen(events)
            pause_b_quit.draw()
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(pause_b, (0, 0, 255), (0, 0, 750, 600), 15)
            pygame.draw.rect(pause_b, (0, 0, 255), (403, 503, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (403, 363, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (53, 363, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (53, 503, 295, 55), 7)
            screen.blit(cursor, (x + 240, y + 100))
        else:
            player.update()
            obstacle = Obstacle()
            obstacle.rect.x = random.randint(-2360, 3640)
            obstacle.rect.y = random.randint(-2520, 3480)
            if not (0 < obstacle.rect.x < 1280 and 0 < obstacle.rect.y < 960):
                obstacles.add(obstacle)
            if obs_count < 60:
                obs_count += 1
            if random.randint(1, 50) == 1:
                gem = Gem()
                gem.rect.x = random.randint(-2360, 3640)
                gem.rect.y = random.randint(-2520, 3480)
                if not (0 < gem.rect.x < 1280 and 0 < gem.rect.y < 960):
                    gems.add(gem)
            camera.update(player)
            score += 0.1
            score_text = pygame.font.Font(None, 60).render('Счёт: ' + str(round(score)), True, (255, 255, 255))
        screen.blit(score_text, (5, 20))
        clock.tick(fps)
        pygame.display.update()
    while menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                menu = False
                con.close()
                quit()
        x, y = pygame.mouse.get_pos()
        bg_menu = pygame.transform.scale(pygame.image.load(os.path.join(
            'images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_menu, (0, 0))
        screen.blit(money_image, (1200, 5))
        screen.blit(volume_image, (0, 885))
        # Отрисовка слайдера, кнопки и вызов функции
        volume_slider.listen(events)
        volume_slider.draw()
        volume()
        menu_b_profiles.listen(events)
        menu_b_profiles.draw()
        menu_b_start.listen(events)
        menu_b_start.draw()
        menu_b_hangar.listen(events)
        menu_b_hangar.draw()
        menu_b_top.listen(events)
        menu_b_top.draw()
        menu_b_quit.listen(events)
        menu_b_quit.draw()
        pygame.draw.rect(screen, (0, 0, 255), (440, 200, 400, 70), 11)
        pygame.draw.rect(screen, (0, 0, 255), (440, 350, 400, 70), 11)
        pygame.draw.rect(screen, (0, 0, 255), (440, 500, 400, 70), 11)
        pygame.draw.rect(screen, (0, 0, 255), (440, 650, 400, 70), 11)
        pygame.draw.rect(screen, (0, 0, 255), (0, 0, 200, 40), 5)
        screen.blit(cursor, (x, y))
        pygame.display.update()
    while profile:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                profile = False
                con.close()
                quit()
        x, y = pygame.mouse.get_pos()
        bg_menu = pygame.transform.scale(pygame.image.load(os.path.join(
            'images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_menu, (0, 0))
        profiles.fill((0, 80, 199))
        profiles.set_alpha(75)
        screen.blit(profiles, (240, 100))
        profiles_b.set_colorkey('BLACK')
        screen.blit(profiles_b, (240, 100))
        profile_1.listen(events)
        profile_1.draw()
        profile_2.listen(events)
        profile_2.draw()
        profile_3.listen(events)
        profile_3.draw()
        profile_4.listen(events)
        profile_4.draw()
        menu_prof.listen(events)
        menu_prof.draw()
        pygame.draw.rect(profiles_b, (0, 0, 255), (0, 0, 750, 800), 15)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 100, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 250, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 400, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 550, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (210, 700, 335, 55), 7)
        screen.blit(cursor, (x + 240, y + 100))
        pygame.display.update()
