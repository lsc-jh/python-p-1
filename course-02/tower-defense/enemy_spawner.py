from enemy import Enemy


class EnemySpawner:
    def __init__(self, path, spawn_rate=1000, max_enemies=10, enemy_speed=2, enemy_max_hp=100):
        self.path = path
        self.enemy_speed = enemy_speed
        self.enemy_max_hp = enemy_max_hp
        self.spawn_rate = spawn_rate
        self.max_enemies = max_enemies
        self.spawn_timer = 0
        self.spawned_enemies = 0
        self.enemies = []

    def update(self, dt, callback):
        for e in self.enemies:
            e.update(callback)

        self.enemies = [e for e in self.enemies if not e.reached_end]
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_rate and self.spawned_enemies < self.max_enemies:
            self.spawn_timer = 0
            enemy = Enemy(self.path, max_hp=self.enemy_max_hp, speed=self.enemy_speed)
            self.enemies.append(enemy)
            self.spawned_enemies += 1

    def draw(self, screen):
        for e in self.enemies:
            e.draw(screen)

    def get_enemy_count(self):
        return len(self.enemies)
