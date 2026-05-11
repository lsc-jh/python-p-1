import pygame
from tileforge import Renderer, Map, Tileset
import json

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 3


class GameMap:
    def __init__(self, path):
        with open(path) as f:
            data = json.load(f)
        self.tileset = Tileset(data["tileset"], data["tile_size"])
        self.tileset.add_property_set(1, set(data["blocked_tiles"]))
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


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy

        tile_size = game_map.renderer.render_tile_size

        corners = [
            (new_x, new_y),
            (new_x + self.size, new_y + self.size),
            (new_x + self.size, new_y),
            (new_x, new_y + self.size),
        ]

        for cx, cy in corners:
            tile_x = cx // tile_size
            tile_y = cy // tile_size
            if game_map.is_blocked(tile_x, tile_y):
                return

        self.x = new_x
        self.y = new_y

    def draw(self, screen, cam_x, cam_y):
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.x - cam_x, self.y - cam_y, self.size, self.size),
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_map = GameMap("map.json")
    game_map.tileset.load()

    start_x = game_map.renderer.render_tile_size * 4
    start_y = game_map.renderer.render_tile_size * 4
    player = Player(start_x, start_y, game_map.renderer.render_tile_size // 2)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= PLAYER_SPEED
        if keys[pygame.K_s]:
            dy += PLAYER_SPEED
        if keys[pygame.K_a]:
            dx -= PLAYER_SPEED
        if keys[pygame.K_d]:
            dx += PLAYER_SPEED

        player.move(dx, dy, game_map)

        screen.fill((0, 0, 0))

        game_map.draw(screen, 0, 0)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
