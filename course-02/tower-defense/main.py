import pygame
from collections import deque
from enemy_spawner import EnemySpawner
from tower import Tower

TILE_SIZE = 50
FPS = 60

TILE_IMAGES = {
    "0": pygame.image.load("assets/grass.png")
}

for key, image in TILE_IMAGES.items():
    TILE_IMAGES[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


def load_map(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        rows = []
        for line in lines:
            clean_line = line.strip()
            row = clean_line.split(' ')
            rows.append(row)

        # one line solution: [line.strip().split() for line in file.readlines()]
        return rows


def extract_path(grid: list[list[str]]):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    start = None

    for cell in grid[rows - 1]:
        if cell == '1':
            start = (grid[rows - 1].index(cell), rows - 1)
            break

    if not start:
        raise ValueError("No starting point found in the last row.")

    path = []
    q = deque([start])
    visited[start[1]][start[0]] = True

    while q:
        c, r = q.popleft()
        x = c * TILE_SIZE + TILE_SIZE // 2
        y = r * TILE_SIZE + TILE_SIZE // 2
        path.append((x, y))

        for dx, dy in directions:
            new_r = r + dy
            new_c = c + dx
            if 0 <= new_r < rows and 0 <= new_c < cols and not visited[new_r][new_c]:
                if grid[new_r][new_c] == '1':
                    visited[new_r][new_c] = True
                    q.append((new_c, new_r))

    return path


def draw_map(screen, grid: list[list[str]]):
    colors = {
        "1": (145, 145, 145),
        "2": (255, 238, 0)
    }

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell = grid[row][col]
            if cell not in colors.keys():
                screen.blit(TILE_IMAGES.get(cell), (col * TILE_SIZE, row * TILE_SIZE))
                continue
            color = colors.get(cell, (255, 0, 0))
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )


def get_col_row(position):
    x, y = position
    col, row = x // TILE_SIZE, y // TILE_SIZE
    return col, row


def get_tower_pos(position):
    col, row = get_col_row(position)
    tx = col * TILE_SIZE + (TILE_SIZE // 2)
    ty = row * TILE_SIZE + (TILE_SIZE // 2)

    return tx, ty


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

    coins = 250
    lives = 10

    def enemy_reached_end(enemy):
        nonlocal lives
        lives -= 1

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
        for t in towers:
            t.update(dt, spawner.enemies)

        draw_map(screen, grid)
        spawner.draw(screen)
        for t in towers:
            t.draw(screen)

        draw_hud(screen, coins, lives)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
