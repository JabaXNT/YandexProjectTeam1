import pygame
import os


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.stage = 1
        self.explosion = pygame.image.load(os.path.join('images\\Space\\explosion\\' + str(int(self.stage // 1)) + '.png')).convert_alpha()
        self.rect = self.explosion.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        if self.stage < 8:
            self.stage += 0.4
        self.explosion = pygame.image.load(os.path.join('images\\Space\\explosion\\' + str(int(self.stage // 1)) + '.png')).convert_alpha()