import pygame

from enemy import Enemy


class EnemySpawner(pygame.sprite.Group):
    def __init__(self, path, spawn_rate=1000, max_enemies=10, enemy_speed=2, enemy_max_hp=100):
        super().__init__()
        self.path = path
        self.enemy_speed = enemy_speed
        self.enemy_max_hp = enemy_max_hp
        self.spawn_rate = spawn_rate
        self.max_enemies = max_enemies
        self.spawn_timer = 0
        self.spawned_enemies = 0
        self.is_wave_active = True
        self.enemy_sheet = pygame.image.load("assets/slime_sheet_walk.png").convert_alpha()

    def update(self, dt, callback):
        for e in self.sprites():
            e.update(callback)

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate:
            if self.spawned_enemies < self.max_enemies:
                self.spawn_timer = 0
                enemy = Enemy(self.enemy_sheet, self.path, max_hp=self.enemy_max_hp, speed=self.enemy_speed)
                self.add(enemy)
                self.spawned_enemies += 1
            elif self.spawned_enemies == self.max_enemies and len(self.sprites()) == 0:
                self.is_wave_active = False

    def update_wave(self, max_enemies, enemy_speed, enemy_max_hp, spawn_rate):
        self.max_enemies = max_enemies
        self.spawn_rate = spawn_rate
        self.enemy_speed = enemy_speed
        self.enemy_max_hp = enemy_max_hp
        self.spawned_enemies = 0
        self.is_wave_active = True
        self.spawn_timer = 0

    def draw(self, surface, bg_surf=None, special_flags=0):
        super().draw(surface, bg_surf, special_flags)
        for e in self.sprites():
            e.draw_health_bar(surface)

    def get_enemy_count(self):
        return len(self.sprites())

    def get_unspawned_count(self):
        return self.max_enemies - self.spawned_enemies
