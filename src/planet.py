import pygame


class Planet(pygame.sprite.Sprite):
    def __init__(self, image, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = 1500
        self.rect.y = 0
