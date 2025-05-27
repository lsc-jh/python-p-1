import pygame

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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        draw_map(screen, grid)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()