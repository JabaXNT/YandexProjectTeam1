import pygame
import os
from pygame_widgets import Button
from src.player import Player


def load_image(name):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


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
    menu = True
    running = False
    running_pause = False


def unpause():
    global running_pause
    running_pause = False


def restart():
    global player
    global all_sprites
    player = Player()
    all_sprites.add(player)


pygame.init()
pygame.mixer.init()
fps = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 960))
pause_b = pygame.Surface((750, 600))
pause = pygame.Surface((750, 600))
all_sprites = pygame.sprite.Group()
pygame.mouse.set_visible(False)
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
                    onClick=restart())
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
                         onClick=lambda: print('Click'))
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
running = False
running_pause = False
menu = True
cursor = load_image('arrow.png').convert_alpha()
while True:
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_pause = True
                if not running_pause:
                    if event.key == pygame.K_LEFT:
                        player.direction = 10
                    if event.key == pygame.K_RIGHT:
                        player.direction = -10
            if event.type == pygame.KEYUP:
                if not running_pause:
                    if event.key == pygame.K_LEFT:
                        player.direction = 0
                    if event.key == pygame.K_RIGHT:
                        player.direction = 0
        bg_running = pygame.transform.scale(load_image('backgrounds\\space.jpg'), (1280, 960))
        screen.blit(bg_running, (0, 0))
        screen.blit(player.image, (player.rect.x + 500, player.rect.y + 500))
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
        clock.tick(fps)
        pygame.display.update()
    while menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                menu = False
                quit()
        x, y = pygame.mouse.get_pos()
        bg_menu = pygame.transform.scale(load_image('backgrounds\\menu.jpg'), (1280, 960))
        screen.blit(bg_menu, (0, 0))
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
        screen.blit(cursor, (x, y))
        pygame.display.update()
