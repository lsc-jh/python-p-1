import pygame
import csv

pygame.init()

# ================== CONFIG ==================
TILE_SIZE = 8      # size in the tileset image (in pixels)
SCALE = 4          # how big we draw it on screen
DRAW_TILE_SIZE = TILE_SIZE * SCALE

MAP_WIDTH = 20
MAP_HEIGHT = 15

PALETTE_COLS = 4   # how many tiles per row in the palette

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# ============================================

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Tile Map Editor")
clock = pygame.time.Clock()

# ---------- Load tileset and slice ----------
def load_tileset(path, tile_size):
    image = pygame.image.load(path).convert_alpha()
    tiles = []
    w, h = image.get_size()

    for y in range(0, h - tile_size + 1, tile_size):
        for x in range(0, w - tile_size + 1, tile_size):
            tile = image.subsurface(pygame.Rect(x, y, tile_size, tile_size))
            tiles.append(tile)

    return tiles

raw_tiles = load_tileset("assets/tileset.png", TILE_SIZE)

# Scale tiles for drawing
tiles = [
    pygame.transform.scale(tile, (DRAW_TILE_SIZE, DRAW_TILE_SIZE))
    for tile in raw_tiles
]

# ---------- Create empty map ----------
level = [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

selected_tile = 0

# ---------- Save / Load ----------
def save_map(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(level)
    print("Map saved to", path)

def load_map(path):
    global level
    with open(path) as f:
        reader = csv.reader(f)
        level = [list(map(int, row)) for row in reader]
    print("Map loaded from", path)

# ---------- Main loop ----------
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_map("map.csv")
            if event.key == pygame.K_l:
                load_map("map.csv")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Click on palette (left side)
            if mx < PALETTE_COLS * DRAW_TILE_SIZE:
                col = mx // DRAW_TILE_SIZE
                row = my // DRAW_TILE_SIZE
                index = row * PALETTE_COLS + col
                if 0 <= index < len(tiles):
                    selected_tile = index

            # Click on map area
            else:
                grid_x = (mx - PALETTE_COLS * DRAW_TILE_SIZE) // DRAW_TILE_SIZE
                grid_y = my // DRAW_TILE_SIZE

                if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                    level[grid_y][grid_x] = selected_tile

    # ---------- Draw ----------
    screen.fill((30, 30, 30))

    # Draw palette
    for i, tile in enumerate(tiles):
        x = (i % PALETTE_COLS) * DRAW_TILE_SIZE
        y = (i // PALETTE_COLS) * DRAW_TILE_SIZE
        screen.blit(tile, (x, y))

        if i == selected_tile:
            pygame.draw.rect(
                screen,
                (255, 255, 0),
                (x, y, DRAW_TILE_SIZE, DRAW_TILE_SIZE),
                2,
            )

    # Draw map
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile_index = level[y][x]
            tile = tiles[tile_index]

            draw_x = PALETTE_COLS * DRAW_TILE_SIZE + x * DRAW_TILE_SIZE
            draw_y = y * DRAW_TILE_SIZE

            screen.blit(tile, (draw_x, draw_y))

            # grid lines
            pygame.draw.rect(
                screen,
                (60, 60, 60),
                (draw_x, draw_y, DRAW_TILE_SIZE, DRAW_TILE_SIZE),
                1,
            )

    pygame.display.flip()

pygame.quit()