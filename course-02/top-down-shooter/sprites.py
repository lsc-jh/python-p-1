import pygame
from helpers import load_images


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, pos, *groups):
        super().__init__(*groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.anim_speed = 10

    def animate(self, dt):
        self.frame_index += self.anim_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]


class Player(AnimatedSprite):
    def __init__(self, x, y, all_sprites, bullets):
        self.frames = load_images("assets/player/walk_")
        super().__init__(self.frames, (x, y), all_sprites)

        self.speed = 250
        self.bullets = bullets
        self.cooldown = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w]: direction.y -= 1
        if keys[pygame.K_s]: direction.y += 1
        if keys[pygame.K_a]: direction.x -= 1
        if keys[pygame.K_d]: direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()
            self.rect.center += direction * self.speed * dt
            self.animate(dt)

        self.cooldown -= dt

        if pygame.mouse.get_pressed()[0] and self.cooldown <= 0:
            self.shoot()
            self.cooldown = 0.2

    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse_pos) - self.rect.center
        if direction.length() > 0:
            direction = direction.normalize()
            Bullet(self.rect.center, direction, self.groups()[0], self.bullets)


class Enemy(AnimatedSprite):
    def __init__(self, x, y, all_sprites, enemies, player):
        self.frames = load_images("assets/enemies/enemy_")
        super().__init__(self.frames, (x, y), all_sprites, enemies)
        self.player = player
        self.speed = 120
        self.health = 3

    def update(self, dt):
        direction = pygame.Vector2(self.player.rect.center) - self.rect.center
        if direction.length() > 0:
            direction = direction.normalize()
            self.rect.center += direction * self.speed * dt
            self.animate(dt)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((6, 6))
        self.image.fill((255, 200, 50))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = 600

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if not pygame.display.get_surface().get_rect().collidepoint(self.rect.center):
            self.kill()
