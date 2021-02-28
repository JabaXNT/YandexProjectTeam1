import pygame
import os
import random


class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randint(1, 3)
        if self.type == 1:
            self.image = pygame.image.load(os.path.join('data\\images\\Space\\bonus\\boost.png')).convert_alpha()
        elif self.type == 2:
            self.image = pygame.image.load(os.path.join('data\\images\\Space\\bonus\\double_gems.png')).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join('data\\images\\Space\\bonus\\shield.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
