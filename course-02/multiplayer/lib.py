from tileforge import Renderer, Map, Tileset
import pygame

PLAYER_SIZE = 24
BULLET_SIZE = 6

def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    return value


def draw_players(screen, players, camera, my_player_id):
    for player_id, player in players.items():
        if not player["alive"]:
            continue

        color = (255, 0, 0)

        if player_id == my_player_id:
            color = (80, 160, 255)

        pygame.draw.rect(
            screen,
            color,
            (
                player["x"] - camera.x,
                player["y"] - camera.y,
                PLAYER_SIZE,
                PLAYER_SIZE,
            ),
        )


def draw_bullets(screen, bullets, camera):
    for bullet in bullets:
        pygame.draw.circle(
            screen,
            (225, 70, 255),
            (
                int(bullet["x"] - camera.x),
                int(bullet["y"] - camera.y),
            ),
            BULLET_SIZE,
        )


def draw_ui(screen, font, my_player):
    if my_player is None:
        return

    hp_text = font.render(f"HP: {my_player['hp']}", True, (255, 255, 255))
    screen.blit(hp_text, (16, 16))

    if not my_player["alive"]:
        dead_text = font.render("YOU DIED", True, (255, 80, 80))
        screen.blit(
            dead_text,
            (
                screen.get_width() // 2 - dead_text.get_width() // 2,
                screen.get_height() // 2 - dead_text.get_height() // 2,
            ),
        )

class GameMap:
    def __init__(self, data):
        self.tileset = Tileset("TILES.png", data["tile_size"])
        self.tileset.add_property_set(1, set(data["blocked_tiles"]))

        width = len(data["layers"][0][0])
        height = len(data["layers"][0])

        self.map = Map(width, height)
        self.map.set_layers(data["layers"])

        self.renderer = Renderer(self.tileset, self.map, 2)

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
        self.renderer.render(screen, (-camera.x, -camera.y))


class Camera:
    def __init__(self, screen_w, screen_h, map_w, map_h):
        self.x = 0
        self.y = 0

        self.screen_w = screen_w
        self.screen_h = screen_h
        self.map_w = map_w
        self.map_h = map_h

    def follow_position(self, x, y):
        wanted_x = x - self.screen_w // 2
        wanted_y = y - self.screen_h // 2

        self.x = clamp(wanted_x, 0, max(0, self.map_w - self.screen_w))
        self.y = clamp(wanted_y, 0, max(0, self.map_h - self.screen_h))

    def screen_to_world(self, screen_x, screen_y):
        return screen_x + self.x, screen_y + self.y

