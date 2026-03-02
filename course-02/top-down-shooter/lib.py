import pygame


def draw_crossed_slot(screen, size, x, y):
    pygame.draw.rect(
        screen,
        (100, 100, 100),
        (x, y, size, size),
        1
    )
    pygame.draw.line(
        screen,
        (100, 100, 100),
        (x, y),
        (x + size, y + size),
        1
    )
    pygame.draw.line(
        screen,
        (100, 100, 100),
        (x + size, y),
        (x, y + size),
        1
    )
