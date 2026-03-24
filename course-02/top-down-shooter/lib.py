from collections.abc import Callable
import pygame
from pygame import Surface

Layer = list[list[tuple[int, int]]]

def draw_map(
        screen: Surface,
        tiles: list[Surface],
        layers: list[Layer],
        map_size: tuple[int, int],
        size,
        offset: tuple[int, int] = (0, 0),
        callback: Callable[[int, int, int, int], None] | None = None
) -> None:
    width, height = map_size
    offset_x, offset_y = offset
    for y in range(height):
        for x in range(width):
            draw_x = x * size + offset_x
            draw_y = y * size + offset_y

            for layer in layers:
                if y >= len(layer) or x >= len(layer[y]):
                    continue
                index, rotation = layer[y][x]
                tile = pygame.transform.rotate(tiles[index], -90 * rotation)
                screen.blit(tile, (draw_x, draw_y))

            if callback:
                try:
                    callback(x, y, draw_x, draw_y)
                except Exception as e:
                    print(f"Error in callback for tile ({x}, {y}): {e}")