import pygame
from enemy_spawner import EnemySpawner
from tower import Tower
from lib import extract_path, get_tower_pos, get_col_row
import math
import json
from tileforge import Renderer, Tileset, Map

FPS = 60

pygame.init()
pygame.font.init()


def tint_multiply(surface, tint_color):
    out = surface.copy()
    out.fill((*tint_color, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return out


def draw_hud(screen, coins, lives, wave, enemies_left):
    hud_h = 40
    surface = pygame.Surface((screen.get_width(), hud_h), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 140))
    screen.blit(surface, (0, 0))

    text = f"Coins: {coins}  Lives: {lives} Wave: {wave}"
    font = pygame.font.SysFont(None, 24)
    rendered = font.render(text, True, (255, 255, 255))
    screen.blit(rendered, (10, 8))

    right_text = f"Enemies Left: {enemies_left}"
    right_rendered = font.render(right_text, True, (255, 255, 255))
    screen.blit(right_rendered, (screen.get_width() - right_rendered.get_width() - 10, 8))


def draw_game_over(screen):
    title_font = pygame.font.SysFont(None, 64)
    subtitle_font = pygame.font.SysFont(None, 32)

    title_text = title_font.render("GAME OVER", True, (255, 0, 0))
    subtitle_text = subtitle_font.render("Press ESC to exit", True, (255, 255, 255))

    t_x = ((screen.get_width() - title_text.get_width()) // 2)
    t_y = ((screen.get_height() - title_text.get_height()) // 2)
    screen.blit(title_text, (t_x, t_y))

    s_x = ((screen.get_width() - subtitle_text.get_width()) // 2)
    s_y = ((screen.get_height() + title_text.get_height()) // 2)
    screen.blit(subtitle_text, (s_x, s_y))


def main():
    with open("map.json", "r") as f:
        data = json.load(f)
    grid = data["bottom_grid"]
    grid = [[str(cell) for cell in row] for row in grid]

    board = [row[:] for row in grid]
    tile_size = data.get("tile_size", 16)
    tileset = Tileset(data["tileset"], tile_size)
    tileset.add_property_set(1, set(data["blocked_tiles"]))
    tileset.add_property_set(2, set(data["pathfinding_tiles"]))
    layout = Map(len(grid[0]), len(grid))
    layout.set_layers(data["layers"])
    renderer = Renderer(tileset, layout, 3)

    window_size = (len(grid[0]) * renderer.render_tile_size, len(grid) * renderer.render_tile_size)

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Tower Defense Game")

    tileset.load()

    clock = pygame.time.Clock()
    running = True

    path = extract_path(layout, renderer.render_tile_size)
    spawner = EnemySpawner(path, spawn_rate=1000, max_enemies=5, enemy_speed=1, enemy_max_hp=30)
    towers = []
    tower = None

    wave = 1
    coins = 180
    lives = 10
    game_over = False

    def enemy_reached_end(enemy):
        nonlocal lives
        nonlocal game_over
        lives -= 1
        if lives <= 0:
            game_over = True

    def enemy_got_killed(enemy):
        nonlocal coins

        earned = max(1, min(35, int(4 + 0.02 * enemy.max_hp)))
        coins += earned

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and game_over:
                running = False
            if game_over:
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if tower:
                    towers.remove(tower)
                    tower = None
                col, row = get_col_row(event.pos, renderer.render_tile_size)
                if grid[row][col] == '1' or board[row][col] == 'T' or coins < 70:
                    continue
                tx, ty = get_tower_pos(event.pos, renderer.render_tile_size)
                tower = Tower(70, tx, ty)
                towers.append(tower)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                col, row = get_col_row(event.pos, renderer.render_tile_size)
                if not tower or grid[row][col] == '1' or board[row][col] == 'T':
                    continue
                tower.is_placed_on_map = True
                board[row][col] = 'T'
                coins -= tower.price
                tower = None

            if event.type == pygame.MOUSEMOTION:
                if not tower:
                    continue
                tx, ty = get_tower_pos(event.pos, renderer.render_tile_size)
                tower.pos = (tx, ty)

        screen.fill((0, 0, 0))
        if not game_over:
            spawner.update(dt, enemy_reached_end)
            if not spawner.is_wave_active:
                wave += 1
                enemy_max_hp = int(40 * (1.12 ** (wave - 1)))
                max_enemies = int(8 + 1.4 * wave + min(12, 4 * math.log2(1 + wave)))
                enemy_speed = min(4, 1 + (wave // 5))
                target_wave_seconds = min(26.0, 10.0 + 0.7 * wave)
                spawn_rate_ms = (target_wave_seconds * 1000.0) / max(1, max_enemies)
                spawn_rate_ms *= (1.0 + 0.18 * (enemy_speed - 1))
                spawn_rate_ms = int(max(250, min(1000, spawn_rate_ms)))

                spawner.update_wave(
                    max_enemies=max_enemies,
                    enemy_speed=enemy_speed,
                    enemy_max_hp=enemy_max_hp,
                    spawn_rate=spawn_rate_ms
                )

            for t in towers:
                t.update(dt, spawner.sprites(), enemy_got_killed)

        renderer.render(screen)

        spawner.draw(screen)
        for t in towers:
            t.draw(screen)

        draw_hud(screen, coins, lives, wave, spawner.get_enemy_count() + spawner.get_unspawned_count())
        if game_over:
            draw_game_over(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
