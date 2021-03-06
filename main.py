import random
import pygame
import os
import sqlite3
import math
from pygame_widgets import Button, Slider, TextBox
from src.player import Player
from src.camera import Camera
from src.obstacle import Obstacle
from src.gem import Gem
from src.explosion import Explosion
from src.sparkle import Sparkle
from src.bonus import Bonus
from src.planet import Planet


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
    pygame.mouse.set_pos(0, 500)


def running_to_profiles():
    global profile
    global profile_change_name
    profile = True
    profile_change_name = False


def unpause():
    global running_pause
    running_pause = False


def restart():
    global obstacles
    global running_pause
    global camera
    global gems
    global bonuses
    global bonus_count
    global sparkles
    global explosions
    global score
    global money_count
    global is_game_over
    global col
    global player
    global current_ship
    global boost_duration
    global double_gems_duration
    global shield_duration
    global earth
    global mars
    global venus
    global mercury
    global pluto
    global neptune
    global missions
    global mb_trig
    global vis_plan
    vis_plan = []
    mb_trig = False
    mis_res = cur.execute('select id, mission from missions where p' + str(active_profile_id) + ' = 0').fetchall()
    missions = []
    if len(mis_res) > 2:
        for i in range(3):
            missions.append([mis_res[i][0], mis_res[i][1]])
    else:
        for i in range(len(mis_res)):
            missions.append([mis_res[i][0], mis_res[i][1]])
    for m in missions:
        m.append(0)
        if m[0] == 8:
            m.append(250)
        elif m[0] == 4:
            m.append(2)
        elif m[0] == 12:
            m.append(300)
        elif m[0] == 16:
            m.append(20)
        elif m[0] % 4 == 3:
            m.append(1)
        elif m[0] % 4 in (1, 2):
            m.append(int(m[1].split()[3]))
        else:
            m.append(6)
        m.append(0)

    earth.rect.x, earth.rect.y = -263, 350
    mars.rect.x, mars.rect.y = -2117, -5000
    pluto.rect.x, pluto.rect.y = 7481, -4306
    neptune.rect.x, neptune.rect.y = -6884, 3442
    mercury.rect.x, mercury.rect.y = 6660, 1200
    venus.rect.x, venus.rect.y = -263, 4000
    player = Player(current_ship)
    score = 0
    money_count = 0 
    sparkles = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    camera = Camera()
    obstacles = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    bonus_count = [0, 0, 0]
    bonuses = pygame.sprite.Group()
    boost_duration = [0, 0]
    double_gems_duration = [0, 0]
    shield_duration = [0, 0]
    running_pause = False
    is_game_over = False
    col = 9999999999


def volume():
    pygame.mixer.Sound.set_volume(soundtrack_menu, volume_slider.getValue() / 100)


def in_game_volume():
    pygame.mixer.Sound.set_volume(soundtrack_in_game, in_game_volume_slider.getValue() / 100)


def _sfx_volume():
    global sfx
    for i in sfx:
        pygame.mixer.Sound.set_volume(i, in_game_sfx_slider.getValue() / 100)


def on_click_button():
    pygame.mixer.Sound.play(sound_click)


def prof_reset():
    global result
    global profile_1
    global profile_2
    global profile_3
    global profile_4
    global moneys
    global active_value
    global menu_b_profiles
    res = cur.execute('UPDATE data SET name = ?, money = ?, high_score = ?, ships = ? WHERE id = ?',
                      ('profile', 0, 0, '1 0 0 0 0 0', active_profile_id,))
    res = cur.execute('update missions set p' + str(active_profile_id) + ' = 0')
    con.commit()
    result = cur.execute("""SELECT * FROM data""").fetchall()
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
    menu_b_profiles = Button(screen, 0, 0, 200, 40, text='profile',
                             fontSize=40, hoverColour=(78, 163, 39),
                             inactiveColour=(50, 122, 17),
                             pressedColour=(231, 247, 49),
                             textColour=(0, 0, 255),
                             onClick=pick_profile_win)
    active_value = 0
    moneys = font.render(f'{active_value}', False, (100, 255, 100))


def gravitation(planet, obj):
    if planet:
        x_dif = obj.rect.center[0] - planet.rect.center[0]
        y_dif = obj.rect.center[1] - planet.rect.center[1]
        sum_dif = abs(x_dif) + abs(y_dif)
        angle = -round(90 * (x_dif / sum_dif))
        if y_dif > 0:
            angle = 180 - angle
        elif angle < 0:
            angle = 360 + angle
        speedx = math.sin(math.radians(angle)) * 4
        speedy = math.cos(math.radians(angle)) * 4
        obj.rect.x += speedx
        obj.rect.y += speedy


def buy_ship(cost, name, id):
    global moneys
    global no_money
    global list_of_ship_text
    global active_value
    global result
    global current_ship
    res2 = cur.execute(f'SELECT ships FROM data WHERE id = {active_profile_id}').fetchall()
    ships = res2[0][0].split(' ')
    if ships[id - 1] == '1':
        current_ship = [pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}.png')).convert_alpha(),
                        pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}1.png')).convert_alpha(),
                        pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}2.png')).convert_alpha(),
                        pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}3.png')).convert_alpha(),
                        pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}4.png')).convert_alpha(),
                        pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}5.png')).convert_alpha(),
                        pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}6.png')).convert_alpha()]
    else:
        if active_value >= cost:
            active_value -= cost
            ships[id - 1] = '1'
            ships = ' '.join(ships)
            res = cur.execute('UPDATE data SET ships = ? WHERE id = ?', (ships, active_profile_id))
            con.commit()
            moneys = font.render(f'{active_value}', False, (100, 255, 100))
            res2 = cur.execute('UPDATE data SET money = ? WHERE id = ?', (active_value, active_profile_id))
            con.commit()
            no_money = pygame.font.Font(None, 40).render('', True, (255, 255, 255))
            list_of_ship_text[id - 1] = pygame.font.Font(None, 40).render('Куплено', True, (255, 255, 255))
            current_ship = pygame.image.load(os.path.join(f'data\\images\\Ships\\{name}')).convert_alpha()
        else:
            no_money = pygame.font.Font(None, 40).render('Не хватает денег', True, (255, 255, 255))
    result = cur.execute("""SELECT * FROM data""").fetchall()
            

def set_text():
    global result
    global profile_1
    global profile_2
    global profile_3
    global profile_4
    global menu_b_profiles
    global change_name_text
    kekw = prof_change_name.getText()
    res = cur.execute(f'UPDATE data SET name = ? WHERE id = ?', (kekw, active_profile_id))
    con.commit()
    result = cur.execute("""SELECT * FROM data""").fetchall()
    change_name_text = pygame.font.Font(None, 40).render('Сохранено', True, (255, 255, 255))
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
    menu_b_profiles = Button(screen, 0, 0, 200, 40, text=kekw,
                             fontSize=40, hoverColour=(78, 163, 39),
                             inactiveColour=(50, 122, 17),
                             pressedColour=(231, 247, 49),
                             textColour=(0, 0, 255),
                             onClick=pick_profile_win)


def pick_profile_win():
    global profile
    global menu
    profile = True
    menu = False


def change_name():
    global profile_change_name
    global profile
    global change_name_text
    profile = False
    profile_change_name = True
    change_name_text = pygame.font.Font(None, 40).render('Для сохранения нажмите Enter', True, (255, 255, 255))


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
    global active_name
    global menu_b_profiles
    global moneys
    global active_profile_id
    global active_value
    profile = False
    high_score = False
    menu = True
    active_profile_id = id
    active_name = name
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
    'data\\sounds\\imperial_march.wav'))
soundtrack_in_game = pygame.mixer.Sound(os.path.join(
    'data\\sounds\\in_game.mp3'))
sound_explosion_ship = pygame.mixer.Sound(os.path.join(
    'data\\sounds\\explosion_7.wav'))
sound_click = pygame.mixer.Sound(os.path.join(
    'data\\sounds\\click.wav'))
sound_gem = pygame.mixer.Sound(os.path.join(
    'data\\sounds\\gem.mp3'))
sound_mission = pygame.mixer.Sound(os.path.join(
    'data\\sounds\\mission.mp3'))
sound_bonus = pygame.mixer.Sound(os.path.join(
    'data\\sounds\\bonus.wav'))
sfx = [sound_explosion_ship, sound_click, sound_gem, sound_bonus, sound_mission]
money_image = pygame.image.load(os.path.join(
    'data\\images\\Space\\gems\\money.png'))
volume_image = pygame.image.load(os.path.join(
    'data\\images\\volume_icon.png'))
cross = pygame.image.load(os.path.join(
    'data\\images\\cross.png'))
cross = pygame.transform.scale(cross, (60, 40))
volume_image = pygame.transform.scale(volume_image, (75, 75))
ship_1 = pygame.image.load(os.path.join('data\\images\\Ships\\ship1.png'))
ship_1 = pygame.transform.scale(ship_1, (134, 236))
ship_2 = pygame.image.load(os.path.join('data\\images\\Ships\\ship2.png'))
ship_2 = pygame.transform.scale(ship_2, (134, 236))
ship_3 = pygame.image.load(os.path.join('data\\images\\Ships\\ship3.png'))
ship_3 = pygame.transform.scale(ship_3, (134, 236))
ship_4 = pygame.image.load(os.path.join('data\\images\\Ships\\ship4.png'))
ship_4 = pygame.transform.scale(ship_4, (134, 236))
ship_5 = pygame.image.load(os.path.join('data\\images\\Ships\\ship5.png'))
ship_5 = pygame.transform.scale(ship_5, (134, 236))
ship_6 = pygame.image.load(os.path.join('data\\images\\Ships\\ship6.png'))
ship_6 = pygame.transform.scale(ship_6, (134, 236))
money_image = pygame.transform.scale(money_image, (75, 75))
money_image_s =pygame.transform.scale(money_image, (65, 65))
moneys = font.render("0", False, (100, 255, 100))
pygame.mixer.Sound.play(soundtrack_menu, loops=-1, fade_ms=1000)
pygame.mixer.Sound.play(soundtrack_in_game, loops=-1, fade_ms=1000)
pygame.mixer.Sound.set_volume(soundtrack_menu, 0.4)
pygame.mixer.Sound.set_volume(soundtrack_in_game, 0)
result = cur.execute("""SELECT * FROM data""").fetchall()
active_name = None
fps = 60
game_over_text = pygame.font.Font(None, 70).render('ИГРА ОКОНЧЕНА', True, (0, 0, 255))
change_name_text = pygame.font.Font(None, 40).render('Для сохранения нажмите Enter', True, (255, 255, 255))
no_money = pygame.font.Font(None, 40).render('', True, (255, 255, 255))
active_profile_id = 1
money_count = 0
active_value = result[0][2]
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 960))
game_over = pygame.Surface((800, 300))
game_over_b = pygame.Surface((800, 300))
pause_b = pygame.Surface((750, 600))
pause = pygame.Surface((750, 600))
pause.set_alpha(75)
pause.fill((0, 80, 199))
pause_b.set_colorkey('BLACK')
mis_pass = pygame.Surface((750, 100))
mis_pass.set_alpha(220)
mis_pass.fill((193, 212, 74))
profiles = pygame.Surface((750, 800))
profiles_b = pygame.Surface((750, 800))
profiles_change_name_b = pygame.Surface((750, 800))
profiles_change_name_b_b = pygame.Surface((750, 800))
high_scores = pygame.Surface((750, 800))
high_scores_b = pygame.Surface((750, 800))
hangars = pygame.Surface((1080, 800))
hangars_b = pygame.Surface((1080, 800))
pygame.mouse.set_visible(False)
volume_slider = Slider(
    screen, 100, 920, 200, 20, min=0, max=100, step=10, colour=(150, 150, 150), handleColour=(55, 115, 17))
in_game_volume_slider = Slider(
    pause_b, 65, 350, 270, 21, min=0, max=100, step=5, initial=10, colour=(55, 115, 17), handleColour=(0, 0, 255))
in_game_sfx_slider = Slider(
    pause_b, 415, 350, 270, 21, min=0, max=100, step=5, initial=100, colour=(55, 115, 17), handleColour=(0, 0, 255))
prof_change_name = TextBox(profiles_change_name_b, 75, 100, 600, 80, fontSize=50,
                           borderColour=(255, 0, 0), textColour=(0, 200, 0),
                           onSubmit=set_text, radius=10, borderThickness=3)
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
pause_b_coninue = Button(pause_b, 50, 398, 300, 60, text='Продолжить',
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
pause_b_menu = Button(pause_b, 400, 398, 300, 60, text='В главное меню',
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
menu_prof = Button(profiles_b, 30, 700, 335, 55, text='Вернуться в меню',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease=running_to_menu)
menu_prof_reset = Button(profiles_b, 30, 30, 335, 55, text='Сбросить прогресс',
                   fontSize=40, hoverColour=(78, 163, 39),
                   inactiveColour=(50, 122, 17),
                   pressedColour=(231, 247, 49),
                   textColour=(0, 0, 255),
                   onClick=on_click_button, onRelease= lambda: prof_reset())
menu_prof_change_name_back = Button(profiles_change_name_b, 200, 500, 385, 55, text='Вернуться в профили',
                                    fontSize=40, hoverColour=(78, 163, 39),
                                    inactiveColour=(50, 122, 17),
                                    pressedColour=(231, 247, 49),
                                    textColour=(0, 0, 255),
                                    onClick=on_click_button, onRelease=running_to_profiles)
menu_prof_change_name = Button(profiles_b, 380, 700, 335, 55, text='Сменить имя',
                               fontSize=40, hoverColour=(78, 163, 39),
                               inactiveColour=(50, 122, 17),
                               pressedColour=(231, 247, 49),
                               textColour=(0, 0, 255),
                               onClick=on_click_button, onRelease=change_name)
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
hangar_ship_default = Button(hangars_b, 50, 50, 250, 250, text='',
                             fontSize=40, hoverColour=(78, 163, 39),
                             pressedColour=(231, 247, 49),
                             textColour=(0, 0, 255),
                             onClick=on_click_button, onRelease=lambda: buy_ship(0, 'default.png', 1))
hangar_ship_2 = Button(hangars_b, 420, 50, 250, 250, image=ship_2,
                       fontSize=40, hoverColour=(78, 163, 39),
                       pressedColour=(231, 247, 49),
                       textColour=(0, 0, 255),
                       onClick=on_click_button, onRelease=lambda: buy_ship(50, 'ship2.png', 2))
hangar_ship_3 = Button(hangars_b, 780, 50, 250, 250, image=ship_3,
                       fontSize=40, hoverColour=(78, 163, 39),
                       pressedColour=(231, 247, 49),
                       textColour=(0, 0, 255),
                       onClick=on_click_button, onRelease=lambda: buy_ship(70, 'ship3.png', 3))
hangar_ship_4 = Button(hangars_b, 50, 370, 250, 250, image=ship_4,
                       fontSize=40, hoverColour=(78, 163, 39),
                       pressedColour=(231, 247, 49),
                       textColour=(0, 0, 255),
                       onClick=on_click_button, onRelease=lambda: buy_ship(100, 'ship4.png', 4))
hangar_ship_5 = Button(hangars_b, 420, 370, 250, 250, image=ship_5,
                       fontSize=40, hoverColour=(78, 163, 39),
                       pressedColour=(231, 247, 49),
                       textColour=(0, 0, 255),
                       onClick=on_click_button, onRelease=lambda: buy_ship(150, 'ship5.png', 5))
hangar_ship_6 = Button(hangars_b, 780, 370, 250, 250, image=ship_6,
                       fontSize=40, hoverColour=(78, 163, 39),
                       pressedColour=(231, 247, 49),
                       textColour=(0, 0, 255),
                       onClick=on_click_button, onRelease=lambda: buy_ship(300, 'ship6.png', 6))
current_ship = pygame.image.load(os.path.join('data\\images\\Ships\\ship1.png')).convert_alpha()
boostC = pygame.image.load(os.path.join('data\\images\\space\\bonus\\boostC.png')).convert_alpha()
double_gemsC = pygame.image.load(os.path.join('data\\images\\space\\bonus\\double_gemsC.png')).convert_alpha()
shieldC = pygame.image.load(os.path.join('data\\images\\space\\bonus\\shieldC.png')).convert_alpha()
boostC = pygame.transform.scale(boostC, (70, 70))
double_gemsC = pygame.transform.scale(double_gemsC, (70, 70))
shieldC = pygame.transform.scale(shieldC, (70, 70))
double = pygame.image.load(os.path.join('data\\images\\space\\gems\\double.png')).convert_alpha()
ship_shield = pygame.image.load(os.path.join('data\\images\\space\\bonus\\ship_shield.png')).convert_alpha()
ship_shield = pygame.transform.scale(ship_shield, (150, 150))
player = Player(current_ship)
mis_time = 999999999
running = False
running_pause = False
profile = False
profile_change_name = False
high_score = False
hangar = False
menu = True
cursor = pygame.image.load(os.path.join('data\\images\\arrow.png')).convert_alpha()
planets = pygame.sprite.Group()
earth = Planet(pygame.image.load(os.path.join('data\\images\\Space\\earth.png')), 638)
mars = Planet(pygame.image.load(os.path.join('data\\images\\Space\\mars.png')), 340)
mercury = Planet(pygame.image.load(os.path.join('data\\images\\Space\\mercury.png')), 244)
venus = Planet(pygame.image.load(os.path.join('data\\images\\Space\\venus.png')), 606)
pluto = Planet(pygame.image.load(os.path.join('data\\images\\Space\\pluto.png')), 114)
neptune = Planet(pygame.image.load(os.path.join('data\\images\\Space\\neptune.png')), 1000)
planets.add(earth)
planets.add(mars)
planets.add(mercury)
planets.add(venus)
planets.add(neptune)
planets.add(pluto)
earth_grav = pygame.Surface((1276, 1276))
earth_grav.fill((4, 1, 33))
pygame.draw.circle(earth_grav, (255, 255, 255), (638, 638), radius=638)
earth_grav.set_alpha(50)
mars_grav = pygame.Surface((680, 680))
mars_grav.fill((4, 1, 33))
pygame.draw.circle(mars_grav, (255, 255, 255), (340, 340), radius=340)
mars_grav.set_alpha(50)
mercury_grav = pygame.Surface((488, 488))
mercury_grav.fill((4, 1, 33))
pygame.draw.circle(mercury_grav, (255, 255, 255), (244, 244), radius=244)
mercury_grav.set_alpha(50)
venus_grav = pygame.Surface((1212, 1212))
venus_grav.fill((4, 1, 33))
pygame.draw.circle(venus_grav, (255, 255, 255), (606, 606), radius=606)
venus_grav.set_alpha(50)
pluto_grav = pygame.Surface((228, 228))
pluto_grav.fill((4, 1, 33))
pygame.draw.circle(pluto_grav, (255, 255, 255), (114, 114), radius=114)
pluto_grav.set_alpha(50)
neptune_grav = pygame.Surface((2000, 2000))
neptune_grav.fill((4, 1, 33))
pygame.draw.circle(neptune_grav, (255, 255, 255), (1000, 1000), radius=1000)
neptune_grav.set_alpha(50)
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
                    if not is_game_over:
                        running_pause = True
                if not running_pause:
                    if event.key == pygame.K_LEFT:
                        player.direction = 5 * rot_koef
                    if event.key == pygame.K_RIGHT:
                        player.direction = -5 * rot_koef
            if event.type == pygame.KEYUP:
                if not running_pause:
                    if event.key == pygame.K_LEFT:
                        player.direction = 0
                    if event.key == pygame.K_RIGHT:
                        player.direction = 0
        pygame.mixer.Sound.set_volume(soundtrack_menu, 0)
        in_game_volume()
        _sfx_volume()
        bg_running = pygame.transform.scale(pygame.image.load(os.path.join(
            'data\\images\\Backgrounds\\space.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_running, (0, 0))
        for sprite in planets:
            if not running_pause and not is_game_over:
                camera.apply(sprite)
            if pygame.sprite.collide_mask(sprite, player):
                explosion = Explosion()
                explosion.rect.x = player.rect.x
                explosion.rect.y = player.rect.y
                explosions.add(explosion)
                pygame.mixer.Sound.play(sound_explosion_ship)
                col = pygame.time.get_ticks()
                res2 = cur.execute(f'SELECT high_score FROM data WHERE id = {active_profile_id}').fetchall()
                if round(score) > res2[0][0]:
                    res = cur.execute(f'UPDATE data SET high_score = {round(score)} WHERE id = {active_profile_id}')
                    con.commit()
                res = cur.execute(
                    f'UPDATE data SET money = {active_value} + {money_count} WHERE id = {active_profile_id}')
                con.commit()
                res2 = cur.execute(f'SELECT money FROM data WHERE id = {active_profile_id}').fetchall()
                active_value = res2[0][0]
                moneys = font.render(f'{res2[0][0]}', False, (100, 255, 100))
                result = cur.execute("""SELECT * FROM data""").fetchall()
            pygame.sprite.groupcollide(planets, gems, False, True)
            pygame.sprite.groupcollide(planets, bonuses, False, True)
            if sprite == neptune:
                if -1000 < sprite.rect.x < 1280 and -1000 < sprite.rect.y < 960:
                    screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
                    if sprite not in vis_plan:
                        vis_plan.append(sprite)
            else:
                if -640 < sprite.rect.x < 1280 and -640 < sprite.rect.y < 960:
                    screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
                    if sprite not in vis_plan:
                        vis_plan.append(sprite)
        screen.blit(earth_grav, (earth.rect.x - 318, earth.rect.y - 318))
        screen.blit(mars_grav, (mars.rect.x - 170, mars.rect.y - 170))
        screen.blit(mercury_grav, (mercury.rect.x - 122, mercury.rect.y - 122))
        screen.blit(venus_grav, (venus.rect.x - 303, venus.rect.y - 303))
        screen.blit(pluto_grav, (pluto.rect.x - 57, pluto.rect.y - 57))
        screen.blit(neptune_grav, (neptune.rect.x - 500, neptune.rect.y - 500))
        screen.blit(player.image, (player.rect.x, player.rect.y))
        for sprite in enumerate(obstacles):
            if not running_pause and not is_game_over:
                camera.apply(sprite[1])
                if sprite[1].update(obstacles):
                    explosion = Explosion()
                    explosion.rect.x = sprite[1].rect.x
                    explosion.rect.y = sprite[1].rect.y
                    explosions.add(explosion)
            if -200 < sprite[1].rect.x < 1280 and -150 < sprite[1].rect.y < 960:
                screen.blit(sprite[1].image, (sprite[1].rect.x, sprite[1].rect.y))
            if (sprite[1].rect.x > 1640 or sprite[1].rect.x < -360) and (
                    sprite[1].rect.y > 1280 or sprite[1].rect.y < -520):
                sprite[1].kill()
            if not running_pause and not is_game_over:
                gravitation(pygame.sprite.spritecollideany(sprite[1], planets,
                                                           collided=pygame.sprite.collide_circle_ratio(1.2)), sprite[1])
            if pygame.sprite.spritecollide(sprite[1], planets, False,
                                           collided=pygame.sprite.collide_circle_ratio(0.65)):
                sprite[1].kill()
                explosion = Explosion()
                explosion.rect.x = sprite[1].rect.x
                explosion.rect.y = sprite[1].rect.y
                explosions.add(explosion)
            if pygame.sprite.collide_mask(player, sprite[1]):
                sprite[1].kill()
                explosion = Explosion()
                explosion.rect.x = player.rect.x
                explosion.rect.y = player.rect.y
                explosions.add(explosion)
                pygame.mixer.Sound.play(sound_explosion_ship)
                if shield_duration[1] > 0:
                    shield_duration[1] = 0
                else:
                    col = pygame.time.get_ticks()
                    res2 = cur.execute(f'SELECT high_score FROM data WHERE id = {active_profile_id}').fetchall()
                    if round(score) > res2[0][0]:
                        res = cur.execute(f'UPDATE data SET high_score = {round(score)} WHERE id = {active_profile_id}')
                        con.commit()
                    res = cur.execute(
                        f'UPDATE data SET money = {active_value} + {money_count} WHERE id = {active_profile_id}')
                    con.commit()
                    res2 = cur.execute(f'SELECT money FROM data WHERE id = {active_profile_id}').fetchall()
                    active_value = res2[0][0]
                    moneys = font.render(f'{res2[0][0]}', False, (100, 255, 100))
                    result = cur.execute("""SELECT * FROM data""").fetchall()
                    if missions[0][0] == 8 and missions[0][4] == 0:
                        mia_com = cur.execute(
                            'update missions set p' + str(active_profile_id) + f' = 1 where {missions[0][0]} = id')
                        con.commit()
        for sprite in gems:
            if (sprite.rect.x > 2640 or sprite.rect.x < -1360) and (sprite.rect.y > 1980 or sprite.rect.y < -1020):
                sprite.kill()
            if not running_pause and not is_game_over:
                camera.apply(sprite)
            if pygame.sprite.collide_mask(player, sprite):
                mb_trig = True
                sprite.kill()
                sparkle = Sparkle()
                sparkle.rect.x = player.rect.x
                sparkle.rect.y = player.rect.y
                sparkles.add(sparkle)
                pygame.mixer.Sound.play(sound_gem)
                money_count += 1
                for m in missions:
                    if m[0] % 4 == 2 and m[2] < m[3]:
                        m[2] += 1
                        if double_gems_duration[1] > 0:
                            m[2] += 1
                            money_count += 1
                    elif m[0] == 16 and double_gems_duration[1] > 0 and m[2] < m[3]:
                        m[2] += 2
                        money_count += 1
            if -200 < sprite.rect.x < 1280 and -150 < sprite.rect.y < 960:
                if double_gems_duration[1] > 0:
                    screen.blit(double, (sprite.rect.x - 10, sprite.rect.y - 10))
                screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
            sprite.update()
        for sprite in bonuses:
            if (sprite.rect.x > 2640 or sprite.rect.x < -1360) and (sprite.rect.y > 1980 or sprite.rect.y < -1020):
                sprite.kill()
            if not running_pause and not is_game_over:
                camera.apply(sprite)
            if pygame.sprite.collide_mask(player, sprite):
                mb_trig = True
                sprite.kill()
                pygame.mixer.Sound.play(sound_bonus)
                if sprite.type == 1:
                    boost_duration = [pygame.time.get_ticks(), 10000]
                elif sprite.type == 2:
                    double_gems_duration = [pygame.time.get_ticks(), 10000]
                else:
                    shield_duration = [pygame.time.get_ticks(), 10000]
            if -200 < sprite.rect.x < 1280 and -150 < sprite.rect.y < 960:
                screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
        for sprite in explosions:
            if not running_pause and not is_game_over:
                sprite.update()
                camera.apply(sprite)
            screen.blit(sprite.explosion, (sprite.rect.x, sprite.rect.y))
        for sprite in sparkles:
            if not running_pause:
                sprite.update()
            screen.blit(sprite.sparkle, (sprite.rect.x, sprite.rect.y))
            camera.apply(sprite)
        screen.blit(money_image, (1200, 5))
        if running_pause:
            screen.blit(pause, (240, 100))
            screen.blit(pause_b, (240, 100))
            pause_b.fill((0, 0, 0))
            pause_b_coninue.listen(events)
            pause_b_coninue.draw()
            pause_b_restart.listen(events)
            pause_b_restart.draw()
            pause_b_menu.listen(events)
            pause_b_menu.draw()
            pause_b_quit.listen(events)
            pause_b_quit.draw()
            in_game_volume_slider.listen(events)
            in_game_volume_slider.draw()
            in_game_sfx_slider.listen(events)
            in_game_sfx_slider.draw()
            volume_text = pygame.font.Font(None, 37).render('ГРОМКОСТЬ МУЗЫКИ', True, (255, 255, 255))
            pause_b.blit(volume_text, (58, 300))
            x, y = pygame.mouse.get_pos()
            pygame.draw.rect(pause_b, (0, 0, 255), (0, 0, 750, 600), 15)
            pygame.draw.rect(pause_b, (0, 0, 255), (403, 503, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (403, 400, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (53, 400, 295, 55), 7)
            pygame.draw.rect(pause_b, (0, 0, 255), (53, 503, 295, 55), 7)
            if len(missions) > 2:
                if missions[2][4] == 1:
                    pygame.draw.rect(pause_b, (50, 122, 17), (25, 195, 697, 50))
                pygame.draw.rect(pause_b, (242, 170, 61), (622, 195, 100, 50), 7)
                pygame.draw.rect(pause_b, (242, 170, 61), (25, 195, 80, 50), 7)
                pygame.draw.rect(pause_b, (0, 0, 255), (25, 195, 697, 50), 7)
                pause_b.blit(pygame.font.Font(None, 60).render(str(missions[2][0]), True, (255, 140, 0)), (35, 200))
                m3_cond = str(missions[2][1])
                m3_track = str(missions[2][2]) + '/' + str(missions[2][3])
                if len(m3_cond) > 36:
                    m_temp = m3_cond[:36].rindex(' ')
                    pause_b.blit(pygame.font.Font(None, 36).render(m3_cond[:m_temp], False, (255, 140, 0)), (120, 200))
                    pause_b.blit(pygame.font.Font(None, 36).render(m3_cond[m_temp + 1:], False, (255, 140, 0)), (120, 220))
                else:
                    pause_b.blit(pygame.font.Font(None, 36).render(m3_cond, False, (255, 140, 0)), (120, 200))
                if missions[2][4] != -1:
                    pause_b.blit(pygame.font.Font(None, 220 // len(m3_track)).render(m3_track, True, (255, 140, 0)),
                                 (632, 200))
                else:
                    pause_b.blit(cross, (632, 200))
            if len(missions) > 1:
                if missions[1][4] == 1:
                    pygame.draw.rect(pause_b, (50, 122, 17), (25, 115, 697, 50))
                pygame.draw.rect(pause_b, (242, 170, 61), (25, 115, 80, 50), 7)
                pygame.draw.rect(pause_b, (242, 170, 61), (622, 115, 100, 50), 7)
                pygame.draw.rect(pause_b, (0, 0, 255), (25, 115, 697, 50), 7)
                pause_b.blit(pygame.font.Font(None, 60).render(str(missions[1][0]), True, (255, 140, 0)), (35, 120))
                m2_cond = str(missions[1][1])
                m2_track = str(missions[1][2]) + '/' + str(missions[1][3])
                if len(m2_cond) > 36:
                    m_temp = m2_cond[:36].rindex(' ')
                    pause_b.blit(pygame.font.Font(None, 36).render(m2_cond[:m_temp], False, (255, 140, 0)), (120, 120))
                    pause_b.blit(pygame.font.Font(None, 36).render(m2_cond[m_temp + 1:], False, (255, 140, 0)),
                                 (120, 140))
                else:
                    pause_b.blit(pygame.font.Font(None, 36).render(m2_cond, False, (255, 140, 0)), (120, 120))
                if missions[1][4] != -1:
                    pause_b.blit(pygame.font.Font(None, 220 // len(m2_track)).render(m2_track, True, (255, 140, 0)),
                                 (632, 120))
                else:
                    pause_b.blit(cross, (632, 120))
            if len(missions) > 0:
                if missions[0][4] == 1:
                    pygame.draw.rect(pause_b, (50, 122, 17), (25, 35, 697, 50))
                pygame.draw.rect(pause_b, (242, 170, 61), (622, 35, 100, 50), 7)
                pygame.draw.rect(pause_b, (242, 170, 61), (25, 35, 80, 50), 7)
                pygame.draw.rect(pause_b, (0, 0, 255), (25, 35, 697, 50), 7)
                pause_b.blit(pygame.font.Font(None, 60).render(str(missions[0][0]), True, (255, 140, 0)), (35, 40))
                m1_cond = str(missions[0][1])
                m1_track = str(missions[0][2]) + '/' + str(missions[0][3])
                if len(m1_cond) > 36:
                    m_temp = m1_cond[:36].rindex(' ')
                    pause_b.blit(pygame.font.Font(None, 36).render(m1_cond[:m_temp], False, (255, 140, 0)), (120, 40))
                    pause_b.blit(pygame.font.Font(None, 36).render(m1_cond[m_temp + 1:], False, (255, 140, 0)),
                                 (120, 60))
                else:
                    pause_b.blit(pygame.font.Font(None, 36).render(m1_cond, False, (255, 140, 0)), (120, 40))
                if missions[0][4] != -1:
                    pause_b.blit(pygame.font.Font(None, 220 // len(m1_track)).render(m1_track, True, (255, 140, 0)),
                                 (632, 40))
                else:
                    pause_b.blit(cross, (632, 40))
            else:
                pause_b.blit(pygame.font.Font(None, 80).render('ВСЕ МИССИИ', True, (255, 140, 0)),
                             (188, 60))
                pause_b.blit(pygame.font.Font(None, 80).render('ВЫПОЛНЕНЫ!', True, (255, 140, 0)),
                             (175, 140))
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
            pygame.draw.rect(game_over_b, (0, 0, 255), (0, 0, 800, 300), 15)
            pygame.draw.rect(game_over_b, (0, 0, 255), (53, 173, 295, 55), 7)
            pygame.draw.rect(game_over_b, (0, 0, 255), (453, 173, 295, 55), 7)
            screen.blit(game_over_text, (430, 350))
            screen.blit(cursor, (x + 240, y + 300))
        else:
            score_text = pygame.font.Font(None, 60).render('Счёт: ' + str(round(score)), True, (255, 255, 255))
            if col == 9999999999:
                player.update()
                score += 0.1
                for m in missions:
                    if m[2] < m[3]:
                        if m[0] == 12 and mb_trig:
                            m[4] = -1
                        if m[0] == 8 and round(score) > 250:
                            m[4] = -1
                        if m[0] % 4 == 1 or m[0] in (8, 12):
                            m[2] = round(score)
                        if m[0] == 3:
                            if venus in vis_plan:
                                m[2] += 1
                        elif m[0] == 7:
                            if mars in vis_plan:
                                m[2] += 1
                        elif m[0] == 11:
                            if mercury in vis_plan:
                                m[2] += 1
                        elif m[0] == 15:
                            if neptune in vis_plan:
                                m[2] += 1
                        elif m[0] == 19:
                            if pluto in vis_plan:
                                m[2] += 1
                        elif m[0] == 20:
                            m[2] = len(vis_plan)
                        elif m[0] == 4:
                            m[2] = sum(bonus_count)
                    if m[2] >= m[3] and m[4] == 0 and m[0] != 8:
                        m[4] = 1
                        id_pass = m[0]
                        mia_com = cur.execute(
                            'update missions set p' + str(active_profile_id) + f' = 1 where {m[0]} = id')
                        con.commit()
                        res = cur.execute(
                            f'UPDATE data SET money = {active_value} + 10 WHERE id = {active_profile_id}')
                        con.commit()
                        res2 = cur.execute(f'SELECT money FROM data WHERE id = {active_profile_id}').fetchall()
                        active_value = res2[0][0]
                        moneys = font.render(f'{res2[0][0]}', False, (100, 255, 100))
                        mis_time = 0
                gravitation(pygame.sprite.spritecollideany(player, planets,
                                                           collided=pygame.sprite.collide_circle_ratio(1.2)), player)
                if boost_duration[1] > 0:
                    boost_duration[1] = 10000 - (pygame.time.get_ticks() - boost_duration[0])
                    screen.blit(boostC, (405, 860))
                    pygame.draw.rect(screen, (100, 100, 100), (390, 940, 100, 10))
                    pygame.draw.rect(screen, (20, 200, 70),
                                     (390, 940, (10000 - (10000 - boost_duration[1])) // 100, 10))
                    rot_koef = 2
                    player.speed_koef = 2
                    bonus_count[0] = 1
                else:
                    bonus_count[0] = 0
                    rot_koef = 1
                    player.speed_koef = 1
                if double_gems_duration[1] > 0:
                    double_gems_duration[1] = 10000 - (pygame.time.get_ticks() - double_gems_duration[0])
                    screen.blit(double_gemsC, (535, 860))
                    pygame.draw.rect(screen, (100, 100, 100), (520, 940, 100, 10))
                    pygame.draw.rect(screen, (20, 200, 70),
                                     (520, 940, (10000 - (10000 - double_gems_duration[1])) // 100, 10))
                    bonus_count[1] = 1
                else:
                    bonus_count[1] = 0
                if shield_duration[1] > 0:
                    bonus_count[2] = 1
                    shield_duration[1] = 10000 - (pygame.time.get_ticks() - shield_duration[0])
                    screen.blit(shieldC, (675, 860))
                    pygame.draw.rect(screen, (100, 100, 100), (660, 940, 100, 10))
                    pygame.draw.rect(screen, (20, 200, 70),
                                     (660, 940, (10000 - (10000 - shield_duration[1])) // 100, 10))
                    screen.blit(ship_shield, (565, 405))
                else:
                    bonus_count[2] = 0
            else:
                player.image = pygame.image.load(os.path.join('data\\images\\Space\\explosion\\8.png')).convert_alpha()
            obstacle = Obstacle()
            obstacle.rect.x = random.randint(-1360, 1640)
            obstacle.rect.y = random.randint(-520, 1280)
            if not (-200 < obstacle.rect.x < 1280 and -200 < obstacle.rect.y < 960):
                obstacles.add(obstacle)
            if random.randint(1, 50) == 1:
                gem = Gem()
                gem.rect.x = random.randint(-1360, 2640)
                gem.rect.y = random.randint(-1020, 1980)
                if not (0 < gem.rect.x < 1280 and 0 < gem.rect.y < 960):
                    gems.add(gem)
            if random.randint(1, 100) == 1:
                bonus = Bonus()
                bonus.rect.x = random.randint(-1360, 2640)
                bonus.rect.y = random.randint(-1020, 1980)
                if not (0 < bonus.rect.x < 1280 and 0 < bonus.rect.y < 960):
                    bonuses.add(bonus)
            if pygame.time.get_ticks() - 800 > col:
                is_game_over = True
        if mis_time < 999999999:
            mis_time += 1
            if mis_time < 33:
                screen.blit(mis_pass, (240, -100 + mis_time * 3))
                pygame.draw.rect(screen, (0, 0, 255), (240, -100 + mis_time * 3, 750, 100), 7)
                screen.blit(pygame.font.Font(None, 52).render('Миссия ' + str(id_pass) + ' успешно заершена!',
                                                              False, (0, 0, 255)), (260, -100 + mis_time * 3 + 37))
                screen.blit(pygame.font.Font(None, 80).render('+10', False, (66, 173, 0)),
                            (816, -100 + mis_time * 3 + 22))
                screen.blit(money_image_s, (910, -100 + mis_time * 3 + 12))
            elif mis_time < 100:
                if mis_time == 34:
                    pygame.mixer.Sound.play(sound_mission)
                screen.blit(mis_pass, (240, 0))
                pygame.draw.rect(screen, (0, 0, 255), (240, 0, 750, 100), 7)
                screen.blit(pygame.font.Font(None, 52).render('Миссия ' + str(id_pass) + ' успешно заершена!',
                                                              False, (0, 0, 255)), (260, 37))
                screen.blit(pygame.font.Font(None, 80).render('+10', False, (66, 173, 0)), (816, 22))
                screen.blit(money_image_s, (910, 12))
            elif mis_time < 133:
                screen.blit(mis_pass, (240, 0 - (mis_time - 100) * 3))
                pygame.draw.rect(screen, (0, 0, 255), (240, 0 - (mis_time - 100) * 3, 750, 100), 7)
                screen.blit(pygame.font.Font(None, 52).render('Миссия ' + str(id_pass) + ' успешно заершена!',
                                                              False, (0, 0, 255)), (260, 0 - (mis_time - 100) * 3 + 37))
                screen.blit(pygame.font.Font(None, 80).render('+10', False, (66, 173, 0)),
                            (816, 0 - (mis_time - 100) * 3 + 22))
                screen.blit(money_image_s, (910, 0 - (mis_time - 100) * 3 + 12))
            else:
                mis_time = 999999999
        score_text = pygame.font.Font(None, 60).render('Счёт: ' + str(round(score)), True, (255, 255, 255))
        gem_count_text = pygame.font.Font(None, 130).render(f'{money_count}', True, (100, 255, 100))
        screen.blit(score_text, (5, 20))
        screen.blit(gem_count_text, (1200 - gem_count_text.get_width(), 5))
        clock.tick(fps)
        camera.update(player)
        camera.apply(player)
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
            'data\\images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
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
    while profile_change_name:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                prof_change_name = False
                con.close()
                quit()
        x, y = pygame.mouse.get_pos()
        bg_menu = pygame.transform.scale(pygame.image.load(os.path.join(
            'data\\images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
        screen.blit(bg_menu, (0, 0))
        profiles_change_name_b_b.fill((0, 80, 199))
        profiles_change_name_b_b.set_alpha(75)
        profiles_change_name_b.set_colorkey('BLACK')
        screen.blit(profiles_change_name_b_b, (240, 100))
        screen.blit(profiles_change_name_b, (240, 100))
        prof_change_name.listen(events)
        prof_change_name.draw()
        menu_prof_change_name_back.listen(events)
        menu_prof_change_name_back.draw()
        pygame.draw.rect(profiles_change_name_b, (0, 0, 255), (200, 500, 385, 55), 6)
        pygame.draw.rect(profiles_change_name_b, (0, 0, 255), (0, 0, 750, 800), 15)
        screen.blit(change_name_text, (400, 440))
        screen.blit(cursor, (x + 240, y + 100))
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
            'data\\images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
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
        menu_prof_reset.listen(events)
        menu_prof_reset.draw()
        menu_prof_change_name.listen(events)
        menu_prof_change_name.draw()
        pygame.draw.rect(profiles_b, (0, 0, 255), (30, 30, 335, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (0, 0, 750, 800), 15)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 100, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 250, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 400, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (225, 550, 295, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (30, 700, 335, 55), 7)
        pygame.draw.rect(profiles_b, (0, 0, 255), (380, 700, 335, 55), 7)
        screen.blit(cursor, (x + 240, y + 100))
        pygame.display.update()
    while high_score:
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
            'data\\images\\backgrounds\\menu.jpg')).convert_alpha(), (1280, 960))
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
        bg_menu = pygame.transform.scale(pygame.image.load(os.path.join('data\\images\\Backgrounds\\menu.jpg'))
                                         .convert_alpha(), (1280, 960))
        screen.blit(bg_menu, (0, 0))
        hangars.fill((0, 80, 199))
        hangars.set_alpha(75)
        screen.blit(hangars, (100, 100))
        hangars_b.set_colorkey('BLACK')
        screen.blit(hangars_b, (100, 100))
        res2 = cur.execute(f'SELECT ships FROM data WHERE id = {active_profile_id}').fetchall()
        ships = res2[0][0].split(' ')
        if ships[1] == '1':
            ship_text_2 = pygame.font.Font(None, 40).render('Куплено', True, (255, 255, 255))
        else:
            ship_text_2 = pygame.font.Font(None, 40).render('Цена: 50', True, (255, 255, 255))
        if ships[2] == '1':
            ship_text_3 = pygame.font.Font(None, 40).render('Куплено', True, (255, 255, 255))
        else:
            ship_text_3 = pygame.font.Font(None, 40).render('Цена: 70', True, (255, 255, 255))
        if ships[3] == '1':
            ship_text_4 = pygame.font.Font(None, 40).render('Куплено', True, (255, 255, 255))
        else:
            ship_text_4 = pygame.font.Font(None, 40).render('Цена: 100', True, (255, 255, 255))
        if ships[4] == '1':
            ship_text_5 = pygame.font.Font(None, 40).render('Куплено', True, (255, 255, 255))
        else:
            ship_text_5 = pygame.font.Font(None, 40).render('Цена: 150', True, (255, 255, 255))
        if ships[5] == '1':
            ship_text_6 = pygame.font.Font(None, 40).render('Куплено', True, (255, 255, 255))
        else:
            ship_text_6 = pygame.font.Font(None, 40).render('Цена: 300', True, (255, 255, 255))
        list_of_ship_text = [ship_text_2, ship_text_3, ship_text_4, ship_text_5, ship_text_5, ship_text_6]
        menu_hangar.listen(events)
        menu_hangar.draw()
        hangar_ship_default.listen(events)
        hangar_ship_default.draw()
        hangar_ship_2.listen(events)
        hangar_ship_2.draw()
        hangar_ship_3.listen(events)
        hangar_ship_3.draw()
        hangar_ship_4.listen(events)
        hangar_ship_4.draw()
        hangar_ship_5.listen(events)
        hangar_ship_5.draw()
        hangar_ship_6.listen(events)
        hangar_ship_6.draw()
        pygame.draw.rect(hangars_b, (0, 0, 255), (0, 0, 1080, 800), 15)
        pygame.draw.rect(hangars_b, (0, 0, 255), (50, 700, 335, 55), 5)
        ship_text_1 = pygame.font.Font(None, 40).render('Куплено', True, (255, 255, 255))
        screen.blit(ship_text_1, (220, 410))
        screen.blit(ship_text_2, (590, 410))
        screen.blit(ship_text_3, (950, 410))
        screen.blit(ship_text_4, (220, 730))
        screen.blit(ship_text_5, (590, 730))
        screen.blit(ship_text_6, (950, 730))
        screen.blit(no_money, (500, 800))
        screen.blit(ship_1, (210, 150))
        pygame.draw.rect(screen, (0, 0, 255), (150, 150, 250, 250), 6)
        pygame.draw.rect(screen, (0, 0, 255), (520, 150, 250, 250), 6)
        pygame.draw.rect(screen, (0, 0, 255), (880, 150, 250, 250), 6)
        pygame.draw.rect(screen, (0, 0, 255), (150, 470, 250, 250), 6)
        pygame.draw.rect(screen, (0, 0, 255), (520, 470, 250, 250), 6)
        pygame.draw.rect(screen, (0, 0, 255), (880, 470, 250, 250), 6)
        screen.blit(money_image, (1200, 5))
        screen.blit(moneys, (1200 - moneys.get_width(), 0))
        screen.blit(cursor, (x + 100, y + 100))
        pygame.display.update()
