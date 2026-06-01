import math

import pygame
from tileforge import Renderer, Map, Tileset, get_from_home
import json
from lib import clamp, world_to_tile, tile_to_world_center
from pathfinding import find_path
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 3

BULLET_SPEED = 8
BULLET_SIZE = 6
SHOOT_COOLDOWN = 200

ENEMY_SPEED = 1.2
ENEMY_SIZE = 24
ENEMY_SPAWN_INTERVAL = 1200
ENEMY_SPAWN_PADDING = 160
ENEMY_PATH_UPDATE_INTERVAL = 200


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

    def shoot(self, x, y):
        dx = x - self.center_x
        dy = y - self.center_y

        distance = math.hypot(dx, dy)

        if distance == 0:
            return None

        dx = dx / distance
        dy = dy / distance

        return Bullet(self.center_x, self.center_y, dx, dy)

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (self.x - camera.x, self.y - camera.y, self.size, self.size),
        )


class Bullet:
    def __init__(self, x, y, dir_x, dir_y):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.alive = True

    def update(self, game_map):
        self.x += self.dir_x * BULLET_SPEED
        self.y += self.dir_y * BULLET_SPEED

        tile_x = int(self.x // game_map.tile_size)
        tile_y = int(self.y // game_map.tile_size)

        if game_map.is_blocked(tile_x, tile_y):
            self.alive = False

    def draw(self, screen, camera):
        pygame.draw.circle(
            screen,
            (225, 70, 255),
            (int(self.x - camera.x), int(self.y - camera.y)),
            BULLET_SIZE
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


class Enemy:
    def __init__(self, x, y, game_map, size=ENEMY_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.alive = True
        self.game_map = game_map

        self.path = []
        self.last_path_update = 0

        self.offset_x = random.uniform(
            -game_map.tile_size * 0.15,
            game_map.tile_size * 0.15,
        )
        self.offset_y = random.uniform(
            -game_map.tile_size * 0.15,
            game_map.tile_size * 0.15,
        )

    @property
    def center_x(self):
        return self.x + self.size / 2

    @property
    def center_y(self):
        return self.y + self.size / 2

    def tile_position(self, game_map):
        return world_to_tile(self.center_x, self.center_y, game_map.tile_size)

    def update(self, player, game_map):
        now = pygame.time.get_ticks()

        if now - self.last_path_update >= ENEMY_PATH_UPDATE_INTERVAL:
            self.path = find_path(
                self.tile_position(game_map),
                player.tile_position(game_map),
                game_map,
            )
            self.last_path_update = now

        self.follow_path(game_map)

    def follow_path(self, game_map):
        if not self.path:
            return

        next_tile_x, next_tile_y = self.path[0]

        target_x, target_y = tile_to_world_center(
            next_tile_x,
            next_tile_y,
            game_map.tile_size,
        )

        target_x += self.offset_x
        target_y += self.offset_y

        dx = target_x - self.center_x
        dy = target_y - self.center_y

        distance = math.hypot(dx, dy)

        if distance <= ENEMY_SPEED:
            self.path.pop(0)
            return

        dx /= distance
        dy /= distance

        self.x += dx * ENEMY_SPEED
        self.y += dy * ENEMY_SPEED

    def collides_with_bullet(self, bullet):
        closest_x = clamp(bullet.x, self.x, self.x + self.size)
        closest_y = clamp(bullet.y, self.y, self.y + self.size)

        dx = bullet.x - closest_x
        dy = bullet.y - closest_y

        return dx * dx + dy * dy <= BULLET_SIZE * BULLET_SIZE

    def collides_with_player(self, player):
        return (
                self.x < player.x + player.size
                and self.x + self.size > player.x
                and self.y < player.y + player.size
                and self.y + self.size > player.y
        )

    def draw(self, screen, camera):
        pygame.draw.rect(
            screen,
            (80, 180, 80),
            (
                self.x - camera.x,
                self.y - camera.y,
                self.size,
                self.size,
            ),
        )


def spawn_enemy(game_map, camera):
    for _ in range(50):
        side = random.choice(["top", "bottom", "left", "right"])

        if side == "top":
            x = random.uniform(
                camera.x - ENEMY_SPAWN_PADDING,
                camera.x + camera.screen_w + ENEMY_SPAWN_PADDING,
            )
            y = camera.y - ENEMY_SPAWN_PADDING

        elif side == "bottom":
            x = random.uniform(
                camera.x - ENEMY_SPAWN_PADDING,
                camera.x + camera.screen_w + ENEMY_SPAWN_PADDING,
            )
            y = camera.y + camera.screen_h + ENEMY_SPAWN_PADDING

        elif side == "left":
            x = camera.x - ENEMY_SPAWN_PADDING
            y = random.uniform(
                camera.y - ENEMY_SPAWN_PADDING,
                camera.y + camera.screen_h + ENEMY_SPAWN_PADDING,
            )

        else:
            x = camera.x + camera.screen_w + ENEMY_SPAWN_PADDING
            y = random.uniform(
                camera.y - ENEMY_SPAWN_PADDING,
                camera.y + camera.screen_h + ENEMY_SPAWN_PADDING,
            )

        x = clamp(x, 0, game_map.width_px - ENEMY_SIZE)
        y = clamp(y, 0, game_map.height_px - ENEMY_SIZE)

        tile_x, tile_y = world_to_tile(x, y, game_map.tile_size)

        if not game_map.is_blocked(tile_x, tile_y):
            return Enemy(
                x - ENEMY_SIZE / 2,
                y - ENEMY_SIZE / 2,
                game_map,
            )

    return None


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

    bullets = []
    enemies = []
    last_shot_time = 0
    last_enemy_spawn_time = 0

    running = True
    while running:
        clock.tick(60)

        current_time = pygame.time.get_ticks()

        def shoot():
            nonlocal last_shot_time, current_time

            if current_time - last_shot_time >= SHOOT_COOLDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                target_x, target_y = camera.screen_to_world(mouse_x, mouse_y)
                b = player.shoot(target_x, target_y)
                if b is not None:
                    bullets.append(b)
                    last_shot_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shoot()

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

        if current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL:
            enemy = spawn_enemy(game_map, camera)

            if enemy is not None:
                enemies.append(enemy)

            last_enemy_spawn_time = current_time

        for b in bullets:
            b.update(game_map)

        for enemy in enemies:
            enemy.update(player, game_map)

        for bullet in bullets:
            for enemy in enemies:
                if enemy.alive and bullet.alive and enemy.collides_with_bullet(bullet):
                    enemy.alive = False
                    bullet.alive = False

        for enemy in enemies:
            if enemy.collides_with_player(player):
                print("Player hit!")

        bullets = [b for b in bullets if b.alive]
        enemies = [e for e in enemies if e.alive]

        game_map.draw(screen, camera)

        for b in bullets:
            b.draw(screen, camera)

        for enemy in enemies:
            enemy.draw(screen, camera)

        player.draw(screen, camera)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
