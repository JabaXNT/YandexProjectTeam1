import os
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ship = pygame.image.load(os.path.join('images\\Ships\\begin\\1.png')).convert_alpha()
        self.image = self.ship
        self.rect = self.ship.get_rect()
        self.speed = 0
        self.rot = 0
        self.last_update = pygame.time.get_ticks()
        self.direction = 0

    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speed
        self.rotate()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.direction) % 360
            self.image = pygame.transform.rotate(self.ship, self.rot)
            self.center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.center
