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
    global profile
    global high_score
    global hangar
    pygame.mixer.Sound.set_volume(soundtrack_in_game, 0)
    menu = True
    running = False
    high_score = False
    profile = False
    hangar = False


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
    global is_game_over
    global col
    score = 0
    sparkles = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    player = Player()
    camera = Camera()
    obstacles = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    running_pause = False
    is_game_over = False
    col = 9999999999


def volume():  # функция для изменения звука(вызывется в главном цикле)
    pygame.mixer.Sound.set_volume(soundtrack_menu, volume_slider.getValue() / 100)

def in_game_volume():
    pygame.mixer.Sound.set_volume(soundtrack_in_game, in_game_volume_slider.getValue() / 100)

def on_click_button():
    pygame.mixer.Sound.play(sound_click)


def pick_profile_win():
    global profile
    global menu
    profile = True
    menu = False

def high_score_win():
    global high_score
    global menu
    high_score = True
    menu = False

def hangar_win():
    global menu
    global hangar
    hangar = True
    menu = False

def pick_p(name, value, id):
    global profile
    global high_score
    global menu
    global menu_b_profiles
    global moneys
    global active_profile_id
    global active_value
    profile = False
    high_score = False
    menu = True
    active_profile_id = id
    active_value = value
    menu_b_profiles = Button(screen, 0, 0, 200, 40, text=name,
                             fontSize=40, hoverColour=(78, 163, 39),
                             inactiveColour=(50, 122, 17),
                             pressedColour=(231, 247, 49),
                             textColour=(0, 0, 255),
                             onClick=pick_profile_win)
    moneys = font.render(f'{value}', False, (100, 255, 100))


pygame.init()
pygame.mixer.init()
con = sqlite3.connect(os.path.join('src\\profiles.db'))
cur = con.cursor()
font = pygame.font.Font(None, 130)
soundtrack_menu = pygame.mixer.Sound(os.path.join(
    'images\\imperial_march.wav'))  # путь до музыки в меню
soundtrack_in_game = pygame.mixer.Sound(os.path.join(
    'images\\Sound\\in_game.mp3'))
sound_explosion_ship = pygame.mixer.Sound(os.path.join(
    'images\\Sound\\explosion_7.wav'))
sound_click = pygame.mixer.Sound(os.path.join(
    'images\\Sound\\click.wav'))
sound_gem = pygame.mixer.Sound(os.path.join(
    'images\\Sound\\gem.mp3'))
sound_mission = pygame.mixer.Sound(os.path.join(
    'images\\imperial_march.wav'))
money_image = pygame.image.load(os.path.join(
    'images\\Space\\gems\\money.png'))  # иконка валюты в меню
volume_image = pygame.image.load(os.path.join(
    'images\\volume_icon.png'))  # иконка звука в меню
volume_image = pygame.transform.scale(volume_image, (75, 75))
money_image = pygame.transform.scale(money_image, (75, 75))
moneys = font.render("0", False, (100, 255, 100))
pygame.mixer.Sound.play(soundtrack_menu, loops=-1, fade_ms=1000)
pygame.mixer.Sound.play(soundtrack_in_game, loops=-1, fade_ms=1000)
pygame.mixer.Sound.set_volume(soundtrack_menu, 0.4)
pygame.mixer.Sound.set_volume(soundtrack_in_game, 0)
result = cur.execute("""SELECT * FROM data""").fetchall()
fps = 60
game_over_text = pygame.font.Font(None, 70).render('ИГРА ОКОНЧЕНА', True, (0, 0, 255))
obs_count = 0
nifo = 0
active_profile_id = 1
money_count = 0
active_value = result[0][2]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 960))
game_over = pygame.Surface((800, 300))
game_over_b = pygame.Surface((800, 300))
pause_b = pygame.Surface((750, 600))
pause = pygame.Surface((750, 600))
profiles = pygame.Surface((750, 800))
profiles_b = pygame.Surface((750, 800))
high_scores = pygame.Surface((750, 800))
high_scores_b = pygame.Surface((750, 800))
hangars = pygame.Surface((1080, 800))
hangars_b = pygame.Surface((1080, 800))
pygame.mouse.set_visible(False)
# слайдер, можно дизайн переделать
volume_slider = Slider(screen, 100, 920, 200, 20, min=0, max=100, step=10)
in_game_volume_slider = Slider(pause_b, 100, 300, 550, 20, min=0, max=100, step=5, initial = 10)
menu_b_profiles = Button(screen, 0, 0, 200, 40, text='Профили',
                         fontSize=40, hoverColour=(78, 163, 39),
                         inactiveColour=(50, 122, 17),
                         pressedColour=(231, 247, 49),
                         textColour=(0, 0, 255),
                         onClick=on_click_button, onRelease=pick_profile_win)
menu_b_start = Button(screen, 440, 200, 400, 70, text='Играть',
                      fontSize=40, hoverColour=(78, 163, 39),
                      inactiveColour=(50, 122, 17),
                      pressedColour=(231, 247, 49), radius=20,
                      textColour=(0, 0, 255),
                      onClick=on_click_button, onRelease=menu_to_running)
menu_b_hangar = Button(screen, 440, 350, 400, 70, text='Ангар',
                       fontSize=40, hoverColour=(78, 163, 39),
                       inactiveColour=(50, 122, 17),
                       pressedColour=(231, 247, 49), radius=20,
                       textColour=(0, 0, 255),
                       onClick=on_click_button, onRelease=hangar_win)
menu_b_top = Button(screen, 440, 500, 400, 70, text='Таблица рекордов',
                    fontSize=40, hoverColour=(78, 163, 39),
                    inactiveColour=(50, 122, 17),
                    pressedColour=(231, 247, 49), radius=20,
                    textColour=(0, 0, 255),
                    onClick=on_click_button, onRelease=high_score_win)
menu_b_quit = Button(screen, 440, 650, 400, 70, text='Выйти из игры',
                     fontSize=40, hoverColour=(78, 163, 39),
                     inactiveColour=(50, 122, 17),
                     pressedColour=(231, 247, 49), radius=20,
                     textColour=(0, 0, 255),
                     onClick=on_click_button, onRelease=lambda: pygame.quit())
pause_b_coninue = Button(pause_b, 50, 360, 300, 60, text='Продолжить',
                         fontSize=40, hoverColour=(78, 163, 39),
                         inactiveColour=(50, 122, 17),
                         pressedColour=(231, 247, 49), radius=20,
                         textColour=(0, 0, 255),
                         onClick=on_click_button, onRelease=lambda: unpause())
pause_b_restart = Button(pause_b, 50, 500, 300, 60, text='Заново',
                         fontSize=40, hoverColour=(78, 163, 39),
                         inactiveColour=(50, 122, 17),
                         pressedColour=(231, 247, 49), radius=20,
                         textColour=(0, 0, 255),
                         onClick=on_click_button, onRelease=lambda: restart())
pause_b_menu = Button(pause_b, 400, 360, 300, 60, text='В главное меню',
                      fontSize=40, hoverColour=(78, 163, 39),
                      inactiveColour=(50, 122, 17),
                      pressedColour=(231, 247, 49), radius=20,
                      textColour=(0, 0, 255),
                      onClick=on_click_button, onRelease=lambda: running_to_menu())
pause_b_quit = Button(pause_b, 400, 500, 300, 60, text='Выйти из игры',
                      fontSize=40, hoverColour=(78, 163, 39),
                      inactiveColour=(50, 122, 17),
                      pressedColour=(231, 247, 49), radius=20,
                      textColour=(0, 0, 255),
                      onClick=on_click_button, onRelease=lambda: pygame.quit())
game_over_restart = Button(game_over_b, 50, 170, 300, 60, text='Заново',
                           fontSize=40, hoverColour=(78, 163, 39),
                           inactiveColour=(50, 122, 17),
                           pressedColour=(231, 247, 49), radius=20,
                           textColour=(0, 0, 255),
                           onClick=lambda: restart())
game_over_menu = Button(game_over_b, 450, 170, 300, 60, text='В главное меню',
                        fontSize=40, hoverColour=(78, 163, 39),
                        inactiveColour=(50, 122, 17),
                        pressedColour=(231, 247, 49), radius=20,
                        textColour=(0, 0, 255),
                        onClick=lambda: running_to_menu())
profile_1 = Button(profiles_b, 225, 100, 295, 55, text=f'{result[0][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=lambda: pick_p(result[0][1], result[0][2], result[0][0]))
profile_2 = Button(profiles_b, 225, 250, 295, 55, text=f'{result[1][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=lambda: pick_p(result[1][1], result[1][2], result[1][0]))
profile_3 = Button(profiles_b, 225, 400, 295, 55, text=f'{result[2][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=lambda: pick_p(result[2][1], result[2][2], result[2][0]))
profile_4 = Button(profiles_b, 225, 550, 295, 55, text=f'{result[3][1]}',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=lambda: pick_p(result[3][1], result[3][2], result[3][0]))
menu_prof = Button(profiles_b, 210, 700, 335, 55, text='Вернуться в меню',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=running_to_menu)
menu_high_score = Button(high_scores_b, 210, 700, 335, 55, text='Вернуться в меню',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=running_to_menu)
menu_hangar = Button(hangars_b, 50, 700, 335, 55, text='Вернуться в меню',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=running_to_menu)
running = False
running_pause = False
profile = False
high_score = False
hangar = False
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
        pygame.mixer.Sound.set_volume(soundtrack_menu, 0)
        in_game_volume()
        bg_running = pygame.transform.scale(pygame.image.load(os.path.join(
            'images\\Backgrounds\\space.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_running, (0, 0))
        if not running_pause:
            camera.apply(player)
        if not is_game_over:
            screen.blit(player.image, (player.rect.x, player.rect.y))
        for sprite in enumerate(obstacles):
            if not running_pause and not is_game_over:
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
                pygame.mixer.Sound.play(sound_explosion_ship)
                explosion = Explosion()
                explosion.rect.x = player.rect.x
                explosion.rect.y = player.rect.y
                explosions.add(explosion)
                col = pygame.time.get_ticks()
        for sprite in gems:
            if (sprite.rect.x > 2640 or sprite.rect.x < -1360) and (sprite.rect.y > 2640 or sprite.rect.y < -1360):
                sprite.kill()
            if not running_pause and not is_game_over:
                camera.apply(sprite)
            if pygame.sprite.collide_mask(player, sprite):  #  Гем
                sprite.kill()
                sparkle = Sparkle()
                sparkle.rect.x = player.rect.x
                sparkle.rect.y = player.rect.y
                sparkles.add(sparkle)
                pygame.mixer.Sound.play(sound_gem)
                money_count += 1
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
            in_game_volume_slider.listen(events) # Примерное расположение слайдера, не знаю куда его поместить поэтому пусть пока там висит
            in_game_volume_slider.draw()
            volume_text = pygame.font.Font(None, 60).render('ГРОМКОСТЬ ЗВУКА', True, (255, 255, 255))
            pause_b.blit(volume_text, (225, 250))
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(pause_b, (0, 0, 255), (0, 0, 750, 600), 15)
            pygame.draw.rect(pause_b, (0, 0, 255), (403, 503, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (403, 363, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (53, 363, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (53, 503, 295, 55), 7)
            screen.blit(cursor, (x + 240, y + 100))
        elif is_game_over:
            game_over.fill((0, 50, 200))
            game_over.set_alpha(75)
            screen.blit(game_over, (240, 300))
            game_over_b.set_colorkey('BLACK')
            screen.blit(game_over_b, (240, 300))
            game_over_menu.listen(events)
            game_over_menu.draw()
            game_over_restart.listen(events)
            game_over_restart.draw()
            x, y = pygame.mouse.get_pos()
            score = score
            res2 = cur.execute(f'SELECT high_score FROM data WHERE id = {active_profile_id}').fetchall()
            if round(score) > res2[0][0]:
                res = cur.execute(f'UPDATE data SET high_score = {round(score)} WHERE id = {active_profile_id}')
                con.commit()
            res = cur.execute(f'UPDATE data SET money = {active_value} + {money_count} WHERE id = {active_profile_id}')
            con.commit()
            res2 = cur.execute(f'SELECT money FROM data WHERE id = {active_profile_id}').fetchall()
            print(res2)
            moneys = font.render(f'{res2[0][0]}', False, (100, 255, 100))
            result = cur.execute("""SELECT * FROM data""").fetchall()
            pygame.draw.rect(game_over_b, (0, 0, 255), (0, 0, 800, 300), 15)
            pygame.draw.rect(game_over_b, (0, 0, 255), (53, 173, 295, 55), 7)
            pygame.draw.rect(game_over_b, (0, 0, 255), (453, 173, 295, 55), 7)
            screen.blit(game_over_text, (430, 350))
            screen.blit(cursor, (x + 240, y + 300))
        else:
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
            score_text = pygame.font.Font(None, 60).render('Счёт: ' + str(round(score)), True, (255, 255, 255))
            if col == 9999999999:
                player.update()
                score += 0.1
            else:
                player.image = pygame.image.load(os.path.join('images\\Space\\explosion\\8.png')).convert_alpha()
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
        if pygame.time.get_ticks() - 700 > col:
            is_game_over = True
        score_text = pygame.font.Font(None, 60).render('Счёт: ' + str(round(score)), True, (255, 255, 255))
        gem_count_text = pygame.font.Font(None, 130).render(f'{money_count}', True, (100, 255, 100))
        screen.blit(score_text, (5, 20))
        screen.blit(gem_count_text, (1200 - gem_count_text.get_width(), 5))
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
        screen.blit(moneys, (1200 - moneys.get_width(), 0))
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
    while high_score: # Окно с результатами(в процессе)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                high_score = False
                con.close()
                quit()
        res2 = cur.execute(f'SELECT high_score, name FROM data').fetchall()
        res2.sort()
        x, y = pygame.mouse.get_pos()
        bg_menu = pygame.transform.scale(pygame.image.load(os.path.join(
            'images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_menu, (0, 0))
        high_scores.fill((0, 80, 199))
        high_scores.set_alpha(75)
        screen.blit(high_scores, (240, 100))
        high_scores_b.set_colorkey('BLACK')
        screen.blit(high_scores_b, (240, 100))
        menu_high_score.listen(events)
        menu_high_score.draw()
        pygame.draw.rect(high_scores_b, (0, 0, 255), (0, 0, 750, 800), 15)
        pygame.draw.rect(high_scores_b, (0, 0, 255), (75, 100, 600, 500), 15)
        high_scores_b.fill(pygame.Color(217, 215, 0), pygame.Rect(75, 100, 600, 125))
        high_scores_b.fill(pygame.Color(192, 192, 192), pygame.Rect(75, 225, 600, 125))
        high_scores_b.fill(pygame.Color(205, 127, 50), pygame.Rect(75, 350, 600, 125))
        high_scores_b.fill(pygame.Color(0, 0, 200), pygame.Rect(75, 475, 600, 125))
        score_text_1 = pygame.font.Font(None, 80).render(res2[3][1] + ':', True, (255, 255, 255))
        score_text_2 = pygame.font.Font(None, 80).render(res2[2][1] + ':', True, (255, 255, 255))
        score_text_3 = pygame.font.Font(None, 80).render(res2[1][1] + ':', True, (255, 255, 255))
        score_text_4 = pygame.font.Font(None, 80).render(res2[0][1] + ':', True, (255, 255, 255))
        score_numb_1 = pygame.font.Font(None, 80).render(str(res2[3][0]), True, (255, 255, 255))
        score_numb_2 = pygame.font.Font(None, 80).render(str(res2[2][0]), True, (255, 255, 255))
        score_numb_3 = pygame.font.Font(None, 80).render(str(res2[1][0]), True, (255, 255, 255))
        score_numb_4 = pygame.font.Font(None, 80).render(str(res2[0][0]), True, (255, 255, 255))
        screen.blit(score_text_1, (355, 235))
        screen.blit(score_text_2, (355, 355))
        screen.blit(score_text_3, (355, 485))
        screen.blit(score_text_4, (355, 615))
        screen.blit(score_numb_1, (725, 235))
        screen.blit(score_numb_2, (725, 355))
        screen.blit(score_numb_3, (725, 485))
        screen.blit(score_numb_4, (725, 615))
        pygame.draw.rect(high_scores_b, (0, 0, 255), (210, 700, 335, 55), 7)
        screen.blit(cursor, (x + 240, y + 100))
        pygame.display.update()
    while hangar:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                hangar = False
                con.close()
                quit()
        x, y = pygame.mouse.get_pos()
        bg_menu = pygame.transform.scale(pygame.image.load(os.path.join(
            'images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_menu, (0, 0))
        hangars.fill((0, 80, 199))
        hangars.set_alpha(75)
        screen.blit(hangars, (100, 100))
        hangars_b.set_colorkey('BLACK')
        screen.blit(hangars_b, (100, 100))
        menu_hangar.listen(events)
        menu_hangar.draw()
        pygame.draw.rect(hangars_b, (0, 0, 255), (0, 0, 1080, 800), 15)
        pygame.draw.rect(hangars_b, (0, 0, 255), (50, 700, 335, 55), 5)
        screen.blit(money_image, (1200, 5))
        screen.blit(moneys, (1200 - moneys.get_width(), 0))
        screen.blit(cursor, (x + 100, y + 100))
        pygame.display.update()
