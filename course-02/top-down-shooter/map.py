import pygame

TILE_SIZE = 32


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


class TileMap:
    def __init__(self, all_sprites):
        grass = pygame.image.load("assets/tiles/grass.png").convert()

        for y in range(0, 600, TILE_SIZE):
            for x in range(0, 800, TILE_SIZE):
                Tile((x, y), grass, all_sprites)
