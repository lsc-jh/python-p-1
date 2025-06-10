import pygame
from collections import deque
from enemy_spawner import EnemySpawner
from tower import Tower

TILE_SIZE = 50
FPS = 60


def load_map(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        rows = []
        for line in lines:
            clean_line = line.strip()
            rows.append(clean_line.split())

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
        "0": (54, 194, 91),
        "1": (145, 145, 145),
    }

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell = grid[row][col]
            color = colors.get(cell, (255, 0, 0))
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )


def main():
    grid = load_map("map.txt")
    window_size = (len(grid[0]) * TILE_SIZE, len(grid) * TILE_SIZE)

    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Tower Defense Game")

    clock = pygame.time.Clock()
    running = True

    path = extract_path(grid)
    spawner = EnemySpawner(path)
    center = TILE_SIZE // 2
    towers = [
        Tower(4 * TILE_SIZE + center, 3 * TILE_SIZE + center),
        Tower(3 * TILE_SIZE + center, 11 * TILE_SIZE + center)
    ]

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        spawner.update(dt)
        for t in towers:
            t.update(dt, spawner.enemies)

        draw_map(screen, grid)
        spawner.draw(screen)
        for t in towers:
            t.draw(screen)

        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":
    main()