import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Проект')
    size = 500, 500
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()