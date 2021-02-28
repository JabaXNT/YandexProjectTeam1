import os
import math
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.ship = ship
        self.image = self.ship
        self.rect = self.ship.get_rect()
        devider = self.rect.size[0] / 76
        self.ship = pygame.transform.scale(self.ship, (int(self.rect.size[0] / devider), int(self.rect.size[1] / devider)))
        self.rot = 0
        self.speedy = 0
        self.speedx = 0
        self.last_update = pygame.time.get_ticks()
        self.direction = 0
        self.speed_koef = 1

    def update(self):
        speed = self.get_speed()
        speed = list(map(lambda x: round(x), speed))
        self.rect.x += speed[0]
        self.rect.y += speed[1]
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

    def get_speed(self):
        speedx = -math.sin(math.radians(self.rot)) * 8
        speedy = -math.cos(math.radians(self.rot)) * 8
        if -1 < speedy < 1:
            self.speedy += speedy
            if -1 < self.speedy < 1:
                speedy = 0
            else:
                speedy = self.speedy
        if -1 < speedx < 1:
            self.speedx += speedx
            if -1 < self.speedx < 1:
                speedx = 0
            else:
                speedx = self.speedx
        if 1 < self.speedy or -1 > self.speedy:
            self.speedy = 0
        if 1 < self.speedx or -1 > self.speedx:
            self.speedx = 0
        return [speedx * self.speed_koef, speedy * self.speed_koef]
