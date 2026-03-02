import pygame
import csv
from lib import draw_crossed_slot

TILE_SIZE = 8
SCALE = 5
DRAW_TILE_SIZE = TILE_SIZE * SCALE

MAP_WIDTH = 20
MAP_HEIGHT = 15

PALETTE_COLS = 6
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900


def load_tileset(path, tile_size):
    image = pygame.image.load(path).convert_alpha()
    tiles = []
    w, h = image.get_size()

    for y in range(0, h - tile_size + 1, tile_size):
        for x in range(0, w - tile_size + 1, tile_size):
            tile = image.subsurface((x, y, tile_size, tile_size))
            tiles.append(tile)

    empty_tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    tiles.insert(0, empty_tile)

    return tiles


def save_map(path, level):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(level)
    print(f"Map saved to {path}")


def load_map(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        return [list(map(int, row)) for row in reader]


def draw_palette(screen, tiles, selected_tile):
    rows_visible = SCREEN_HEIGHT // DRAW_TILE_SIZE
    max_slots = PALETTE_COLS * rows_visible

    drawn_tiles = min(len(tiles), max_slots)

    for i in range(drawn_tiles):
        tile = tiles[i]

        x = (i % PALETTE_COLS) * DRAW_TILE_SIZE
        y = (i // PALETTE_COLS) * DRAW_TILE_SIZE

        screen.blit(tile, (x, y))

        if i == selected_tile:
            pygame.draw.rect(
                screen,
                (255, 255, 0),
                (x, y, DRAW_TILE_SIZE, DRAW_TILE_SIZE),
                2
            )

    for i in range(drawn_tiles, max_slots):
        x = (i % PALETTE_COLS) * DRAW_TILE_SIZE
        y = (i // PALETTE_COLS) * DRAW_TILE_SIZE
        draw_crossed_slot(screen, DRAW_TILE_SIZE, x, y)


def draw_map(screen, level, tiles):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_index = level[y][x]
            tile = tiles[tile_index]

            draw_x = PALETTE_COLS * DRAW_TILE_SIZE + x * DRAW_TILE_SIZE
            draw_y = y * DRAW_TILE_SIZE

            screen.blit(tile, (draw_x, draw_y))
            pygame.draw.rect(
                screen,
                (60, 60, 60),
                (draw_x, draw_y, DRAW_TILE_SIZE, DRAW_TILE_SIZE),
                0
            )


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tile Map Editor")
    clock = pygame.time.Clock()

    raw_tiles = load_tileset("assets/tileset.png", TILE_SIZE)

    tiles = [
        pygame.transform.scale(tile, (DRAW_TILE_SIZE, DRAW_TILE_SIZE)) for tile in raw_tiles
    ]

    level = []
    for _ in range(MAP_HEIGHT):
        row = []
        for _ in range(MAP_WIDTH):
            row.append(0)
        level.append(row)

    selected_tile = 0

    running = True
    palette_width = PALETTE_COLS * DRAW_TILE_SIZE

    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_map("map.csv", level)
                elif event.key == pygame.K_l:
                    level = load_map("map.csv")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos

                    if mx < palette_width:
                        col = mx // DRAW_TILE_SIZE
                        row = my // DRAW_TILE_SIZE
                        index = row * PALETTE_COLS + col

                        if 0 <= index < len(tiles):
                            selected_tile = index

        mx, my = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0] and mx >= palette_width:
            grid_x = (mx - palette_width) // DRAW_TILE_SIZE
            grid_y = my // DRAW_TILE_SIZE

            if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                level[grid_y][grid_x] = selected_tile

        if mouse_buttons[2] and mx >= palette_width:
            grid_x = (mx - palette_width) // DRAW_TILE_SIZE
            grid_y = my // DRAW_TILE_SIZE

            if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                level[grid_y][grid_x] = 0

        screen.fill((30, 30, 30))

        draw_palette(screen, tiles, selected_tile)

        draw_map(screen, level, tiles)

        pygame.display.flip()


if __name__ == "__main__":
    main()
