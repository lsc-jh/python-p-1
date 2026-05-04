import pygame
from tileforge import Renderer, Map, Tileset
import json


class GameMap:
    def __init__(self, path):
        with open(path) as f:
            data = json.load(f)
        self.tileset = Tileset(data["tileset"], data["tile_size"])
        self.tileset.add_property_set(1, set(data["blocked_tiles"]))
        self.tileset.load()

        width = len(data["layers"][0][0])
        height = len(data["layers"][0])
        self.map = Map(width, height)
        self.map.set_layers(data["layers"])

        self.renderer = Renderer(self.tileset, self.map, 2)

    def draw(self, screen, cam_x, cam_y):
        offset = (-cam_x, -cam_y)
        self.renderer.render(screen, offset)

    def is_blocked(self, x, y):
        if x < 0 or y < 0 or x >= self.map.width or y >= self.map.height:
            return True
        return self.map.cell_has_property(self.tileset, (x, y), 1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    game_map = GameMap("map.json")

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        game_map.draw(screen, 0, 0)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
