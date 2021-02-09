import pygame
import os


class Sparkle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sparkle = pygame.image.load(os.path.join('images\\Space\\gems\\0.gif')).convert()
        self.rect = self.sparkle.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.stage = 0

    def update(self):
        if self.stage < 8:
            self.stage += 0.4
        else:
            self.kill()
        self.sparkle = pygame.image.load(os.path.join('images\\Space\\gems\\' + str(int(self.stage // 1)) + '.gif')).convert()
        self.sparkle.set_colorkey((77, 77, 77))
        self.sparkle = pygame.transform.scale(self.sparkle, (80, 80))
