import pygame
import sys
import os
from pygame_widgets import Button


def load_image(name):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.init()
screen = pygame.display.set_mode((1280, 960))
all_sprites = pygame.sprite.Group()
b_start = Button(screen, 440, 200, 400, 70, text='Играть',
                 fontSize=40, hoverColour=(78, 163, 39),
                 inactiveColour=(50, 122, 17),
                 pressedColour=(231, 247, 49), radius=20,
                 textColour=(0, 0, 255),
                 onClick=lambda: print('Click'))
b_hangar = Button(screen, 440, 350, 400, 70, text='Ангар',
                  fontSize=40, hoverColour=(78, 163, 39),
                  inactiveColour=(50, 122, 17),
                  pressedColour=(231, 247, 49), radius=20,
                  textColour=(0, 0, 255),
                  onClick=lambda: print('Click'))
b_top = Button(screen, 440, 500, 400, 70, text='Таблица рекордов',
               fontSize=40, hoverColour=(78, 163, 39),
               inactiveColour=(50, 122, 17),
               pressedColour=(231, 247, 49), radius=20,
               textColour=(0, 0, 255),
               onClick=lambda: print('Click'))
b_quit = Button(screen, 440, 650, 400, 70, text='Выйти из игры',
                fontSize=40, hoverColour=(78, 163, 39),
                inactiveColour=(50, 122, 17),
                pressedColour=(231, 247, 49), radius=20,
                textColour=(0, 0, 255),
                onClick=lambda: pygame.quit())
running = False
menu = True
while True:
    while menu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                menu = False
                quit()
        bg_menu = pygame.transform.scale(
            load_image('backgrounds\\menu.jpg'), (1280, 960))
        screen.blit(bg_menu, (0, 0))
        b_start.listen(events)
        b_start.draw()
        b_hangar.listen(events)
        b_hangar.draw()
        b_top.listen(events)
        b_top.draw()
        b_quit.listen(events)
        b_quit.draw()
        pygame.draw.rect(screen, (0, 0, 255), (440, 200, 400, 70), 11)
        pygame.draw.rect(screen, (0, 0, 255), (440, 350, 400, 70), 11)
        pygame.draw.rect(screen, (0, 0, 255), (440, 500, 400, 70), 11)
        pygame.draw.rect(screen, (0, 0, 255), (440, 650, 400, 70), 11)
        pygame.display.update()
