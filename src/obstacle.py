import pygame
import random
import math
import os


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        lst = []
        for i in range(41):
            lst.append(0 + i * 0.1)
        self.koefx = random.choice(lst)
        self.koefy = random.choice(lst)
        self.rot = random.randrange(0, 365)
        if self.koefx + self.koefy < 6:
            self.image = pygame.image.load(os.path.join('images\\space\\asteroid.png'))
            self.image = pygame.transform.rotate(self.image, random.randrange(0, 365))
            self.image = pygame.transform.scale(self.image, (100, 100))
        else:
            self.image = pygame.image.load(os.path.join('images\\space\\comet.png')).convert_alpha()
            self.image = pygame.transform.rotate(self.image, self.rot - 130)
            self.image = pygame.transform.scale(self.image, (159, 142))
        self.rect = self.image.get_rect()
        self.speedy = 0
        self.speedx = 0

    def update(self, obstacles):
        speed = self.get_speed()
        speed = list(map(lambda x: round(x), speed))
        self.rect.x += speed[0]
        self.rect.y += speed[1]
        for obstacle in obstacles:
            if self != obstacle and self.rect.colliderect(obstacle.rect):
                obstacle.kill()
                self.kill()
                return True

    def get_speed(self):
        speedx = -math.sin(math.radians(self.rot)) * self.koefx
        speedy = -math.cos(math.radians(self.rot)) * self.koefy
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
        return [speedx, speedy]