import pygame
import math
from projectile import Projectile


class Tower:
    def __init__(self, price, x, y, range_px=150, fire_rate=1000):
        self.price = price
        self.pos = (x, y)
        self.range = range_px
        self.fire_rate = fire_rate
        self.time_since_last_shot = 0
        self.projectiles = []
        self.is_placed_on_map = False

    def update(self, dt, enemies, callback):
        if not self.is_placed_on_map:
            return

        self.time_since_last_shot += dt

        target = None
        min_dist = float("inf")
        for enemy in enemies:
            if enemy.reached_end:
                continue
            ex, ey = enemy.position
            dist = math.hypot(ex - self.pos[0], ey - self.pos[1])
            if dist <= self.range and dist < min_dist:
                target = enemy
                min_dist = dist

        if target and self.time_since_last_shot >= self.fire_rate:
            self.projectiles.append(Projectile(self.pos, target))
            self.time_since_last_shot = 0

        for p in self.projectiles:
            p.update(callback)

        self.projectiles = [p for p in self.projectiles if not p.hit]

    def draw(self, screen):
        color = None
        if self.is_placed_on_map:
            color = (0, 100, 200)
        else:
            color = (200, 200, 200)

        pygame.draw.circle(screen, color, self.pos, 15)
        pygame.draw.circle(screen, color, self.pos, self.range, 1)
        for p in self.projectiles:
            p.draw(screen)
