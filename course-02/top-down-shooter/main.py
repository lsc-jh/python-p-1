import pygame
from settings import *
from sprites import Player, Enemy, Bullet
from map import TileMap

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def main():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    tilemap = TileMap(all_sprites)

    player = Player(400, 300, all_sprites, bullets)

    for i in range(5):
        Enemy(100 + i * 80, 100, all_sprites, enemies, player)

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update(dt)

        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
