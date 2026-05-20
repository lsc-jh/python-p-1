import pygame
from tileforge import Renderer, Map, Tileset, get_from_home
import json
from lib import clamp, world_to_tile

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

        self.renderer = Renderer(self.tileset, self.map, 1)

    @property
    def tile_size(self):
        return self.renderer.render_tile_size

    @property
    def width_px(self):
        return self.map.width * self.tile_size

    @property
    def height_px(self):
        return self.map.height * self.tile_size

    def load(self):
        self.tileset.load()

    def draw(self, screen, camera):
        offset = (-camera.x, -camera.y)
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

    @property
    def center_x(self):
        return self.x + self.size / 2

    @property
    def center_y(self):
        return self.y + self.size / 2

    def tile_position(self, game_map):
        return world_to_tile(self.center_x, self.center_y, game_map.tile_size)

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

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.x - camera.x, self.y - camera.y, self.size, self.size),
        )


class Camera:
    def __init__(self, screen_w, screen_h, map_w, map_h):
        self.x = 0
        self.y = 0

        self.screen_w = screen_w
        self.screen_h = screen_h

        self.map_w = map_w
        self.map_h = map_h

    def follow(self, target):
        wanted_x = target.center_x - self.screen_w // 2
        wanted_y = target.center_y - self.screen_h // 2

        if self.map_w > self.screen_w:
            self.x = clamp(wanted_x, 0, self.map_w - self.screen_w)
        else:
            self.x = -(self.screen_w - self.map_w) // 2

        if self.map_h > self.screen_h:
            self.y = clamp(wanted_y, 0, self.map_h - self.screen_h)
        else:
            self.y = -(self.screen_h - self.map_h) // 2

    def screen_to_world(self, screen_x, screen_y):
        return screen_x + self.x, screen_y + self.y


def main():
    pygame.init()

    game_map = GameMap(get_from_home("tileset-editor-export.json"))

    screen_width = clamp(game_map.width_px, SCREEN_WIDTH, 800)
    screen_height = clamp(game_map.height_px, SCREEN_HEIGHT, 600)

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    game_map.load()

    start_x = game_map.tile_size * 4
    start_y = game_map.tile_size * 4
    player = Player(start_x, start_y, game_map.tile_size // 2)

    camera = Camera(screen_width, screen_height, game_map.width_px, game_map.height_px)

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

        camera.follow(player)

        screen.fill((0, 0, 0))

        game_map.draw(screen, camera)
        player.draw(screen, camera)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
