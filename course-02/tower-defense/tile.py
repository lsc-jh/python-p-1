import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, kind, images):
        super().__init__()
        self.image = images[kind]
        self.rect = self.image.get_rect(topLeft=(x, y))
        self.kind = kind
