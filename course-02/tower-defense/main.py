import pygame
from enemy_spawner import EnemySpawner
from tower import Tower
from lib import load_map, extract_path, get_tower_pos, get_col_row, TILE_SIZE

FPS = 60


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


def get_image(path):
    image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    image.fill((0, 0, 0))
    loaded_image = pygame.image.load(path)
    scaled_image = pygame.transform.scale(loaded_image, (TILE_SIZE, TILE_SIZE))
    image.blit(scaled_image, (0, 0))
    return image


def draw_map(screen, grid: list[list[str]]):
    grass_image = get_image("assets/grass2.png")
    path_image = get_image("assets/path.jpg")
    tiles = pygame.sprite.Group()

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell = grid[row][col]
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if cell == "0":
                tile = Tile(grass_image, x, y)
            else:
                tile = Tile(path_image, x, y)
            tiles.add(tile)
    tiles.draw(screen)


def draw_hud(screen, coins, lives):
    hud_h = 40
    surface = pygame.Surface((screen.get_width(), hud_h), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 140))
    screen.blit(surface, (0, 0))

    text = f"Coins: {coins}  Lives: {lives}"
    font = pygame.font.SysFont(None, 24)
    rendered = font.render(text, True, (255, 255, 255))
    screen.blit(rendered, (10, 8))


def main():
    grid = load_map("map.txt")
    board = [row[:] for row in grid]

    window_size = (len(grid[0]) * TILE_SIZE, len(grid) * TILE_SIZE)

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Tower Defense Game")

    clock = pygame.time.Clock()
    running = True

    path = extract_path(grid)
    spawner = EnemySpawner(path, spawn_rate=1000, max_enemies=5, enemy_speed=1, enemy_max_hp=30)
    towers = []
    tower = None

    wave = 1
    coins = 250
    lives = 10

    def enemy_reached_end(enemy):
        nonlocal lives
        lives -= 1

    def enemy_got_killed(enemy):
        nonlocal coins

        earned_coins_based_on_hp = min(enemy.max_hp, 250)
        coins += earned_coins_based_on_hp

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if tower:
                    towers.remove(tower)
                    tower = None
                col, row = get_col_row(event.pos)
                if grid[row][col] == '1' or board[row][col] == 'T' or coins < 60:
                    continue
                tx, ty = get_tower_pos(event.pos)
                tower = Tower(60, tx, ty)
                towers.append(tower)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                col, row = get_col_row(event.pos)
                if not tower or grid[row][col] == '1' or board[row][col] == 'T':
                    continue
                tower.is_placed_on_map = True
                board[row][col] = 'T'
                coins -= tower.price
                tower = None

            if event.type == pygame.MOUSEMOTION:
                if not tower:
                    continue
                tx, ty = get_tower_pos(event.pos)
                tower.pos = (tx, ty)

        screen.fill((0, 0, 0))

        spawner.update(dt, enemy_reached_end)
        if not spawner.is_wave_active:
            wave += 1
            max_enemies = 5 + wave * 2
            enemy_max_hp = 30 + wave * 4
            enemy_speed = 1 + wave // 5
            spawner.update_wave(dt, max_enemies=max_enemies, enemy_speed=enemy_speed, enemy_max_hp=enemy_max_hp)

        for t in towers:
            t.update(dt, spawner.sprites(), enemy_got_killed)

        draw_map(screen, grid)
        spawner.draw(screen)
        for t in towers:
            t.draw(screen)

        draw_hud(screen, coins, lives)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
