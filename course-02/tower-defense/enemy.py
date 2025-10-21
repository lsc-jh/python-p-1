import math
import pygame
from lib import TILE_SIZE, get_frame_from_sheet

WALK_DOWN = 0
WALK_UP = 1
WALK_LEFT = 2
WALK_RIGHT = 3

ANIMATION_LENGTH = 8


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, path, speed=2, max_hp=100):
        super().__init__()
        self.direction = WALK_UP
        self.anim_frame = 0
        self.anim_timer = 0

        self.animations = {
            WALK_DOWN: [get_frame_from_sheet(sheet, i, 64, 64, 0) for i in range(ANIMATION_LENGTH)],
            WALK_UP: [get_frame_from_sheet(sheet, i, 64, 64, 1) for i in range(ANIMATION_LENGTH)],
            WALK_LEFT: [get_frame_from_sheet(sheet, i, 64, 64, 2) for i in range(ANIMATION_LENGTH)],
            WALK_RIGHT: [get_frame_from_sheet(sheet, i, 64, 64, 3) for i in range(ANIMATION_LENGTH)]
        }

        self.image = self.animations[self.direction][self.anim_frame]
        self.rect = self.image.get_rect()

        self.path = path
        self.speed = speed
        self.max_hp = max_hp
        self.hp = max_hp
        self.position = list(path[0])
        self.rect.center = (self.position[0], self.position[1])
        self.current_target = 1
        self.reached_end = False

    def _pick_direction(self, dx, dy):
        if abs(dx) > abs(dy):
            self.direction = WALK_RIGHT if dx > 0 else WALK_LEFT
        else:
            self.direction = WALK_DOWN if dy > 0 else WALK_UP

    def _tick_animation(self):
        self.anim_timer += 1
        if self.anim_timer >= self.speed * 4:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % ANIMATION_LENGTH
        self.image = self.animations[self.direction][self.anim_frame]

    def update(self, callback):
        if self.reached_end or self.current_target >= len(self.path):
            self.reached_end = True
            callback(self)
            self.kill()
            return

        target = self.path[self.current_target]
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.position = list(target)
            self.current_target += 1
        else:
            self.position[0] += dx / dist * self.speed
            self.position[1] += dy / dist * self.speed
        self._pick_direction(dx, dy)

        self.rect.center = (int(self.position[0]), int(self.position[1]))
        self._tick_animation()

    def draw_health_bar(self, screen):
        bar_width = 20
        bar_height = 4
        hp_ratio = self.hp / self.max_hp
        x = int(self.position[0] - bar_width / 2)
        y = int(self.position[1] - 18)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, int(bar_width * hp_ratio), bar_height))

    def take_damage(self, amount, callback):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            callback(self)
            self.kill()
