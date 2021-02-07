import pygame
import os


class Gem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.count = 1
        self.image = pygame.image.load(os.path.join('images\\Space\\gems\\1.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()

    def update(self):
        self.image = pygame.image.load(os.path.join('images\\Space\\gems\\' + str(self.count) + '.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.count += 1
        if self.count == 15:
            self.count = 1
