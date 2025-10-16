import math
import pygame
from lib import TILE_SIZE, get_frame_from_sheet

WALK_DOWN = 0
WALK_UP = 1
WALK_LEFT = 2
WALK_RIGHT = 3


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, path, speed=2, max_hp=100):
        super().__init__()
        self.direction = WALK_UP
        self.anim_frame = 0
        self.anim_timer = 0
        self.is_moving = False

        self.animations = {
            WALK_DOWN: [get_frame_from_sheet(sheet, i, 64, 64, 0) for i in range(8)],
            WALK_UP: [get_frame_from_sheet(sheet, i, 64, 64, 1) for i in range(8)],
            WALK_LEFT: [get_frame_from_sheet(sheet, i, 64, 64, 2) for i in range(8)],
            WALK_RIGHT: [get_frame_from_sheet(sheet, i, 64, 64, 3) for i in range(8)]
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

    def update(self, callback):
        if self.reached_end or self.current_target >= len(self.path):
            self.reached_end = True
            callback(self)
            self.kill()

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

        self.rect.center = (int(self.position[0]), int(self.position[1]))

    def take_damage(self, amount, callback):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            callback(self)
            self.kill()
