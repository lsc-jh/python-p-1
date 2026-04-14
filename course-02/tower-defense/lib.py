from collections import deque
from tileforge import Renderer

import pygame

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


def extract_path(renderer: Renderer):
    grid = renderer.__map.get_layer_grid(0)
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    start = None

    tileset = renderer.tileset

    for cell in grid[rows - 1]:
        if tileset.has_property(cell, 2):
            start = (grid[rows - 1].index(cell), rows - 1)
            break

    if not start:
        raise ValueError("No starting point found in the last row.")

    path = []
    q = deque([start])
    visited[start[1]][start[0]] = True

    while q:
        c, r = q.popleft()
        x = c * renderer.render_tile_size + renderer.render_tile_size // 2
        y = r * renderer.render_tile_size + renderer.render_tile_size // 2
        path.append((x, y))

        for dx, dy in directions:
            new_r = r + dy
            new_c = c + dx
            if 0 <= new_r < rows and 0 <= new_c < cols and not visited[new_r][new_c]:
                if tileset.has_property(grid[new_r][new_c], 2):
                    visited[new_r][new_c] = True
                    q.append((new_c, new_r))

    return path


def get_col_row(position, tile_size):
    x, y = position
    col, row = x // tile_size, y // tile_size
    return col, row


def get_tower_pos(position, tile_size):
    col, row = get_col_row(position, tile_size)
    tx = col * tile_size + (tile_size // 2)
    ty = row * tile_size + (tile_size // 2)

    return tx, ty


def get_frame_from_sheet(sheet, frame, width, height, row, color=(0, 0, 0)):
    image = pygame.Surface((width, height))
    image.fill(color)
    image.set_colorkey(color)
    image.blit(sheet, (0, 0), (frame * width, row * height, width, height))
    return image
