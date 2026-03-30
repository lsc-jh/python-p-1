import pygame
import json
from lib import Tileset, Map, Renderer

TILE_SIZE = 16
SCALE = 3

MAP_WIDTH = 20
MAP_HEIGHT = 15

PALETTE_COLS = 5
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

BLOCKED_TILE_TYPE = 1
PATH_TILE_TYPE = 2


def draw_crossed_box(screen, x, y, size, color):
    pygame.draw.rect(screen, color, (x, y, size, size), 1)
    pygame.draw.line(screen, color, (x, y), (x + size, y + size), 1)
    pygame.draw.line(screen, color, (x + size, y), (x, y + size), 1)


# [[[], [], [], [], []], [[], [], [], [], []]]

class Editor:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.selected_layer = 0
        self.selected_tile = 0
        self.current_rotation = 0

        self.show_tile_properties = True

        self.tileset = Tileset("assets/TILES.png", TILE_SIZE)
        self.tileset.load()
        self.map = Map(MAP_WIDTH, MAP_HEIGHT, self.tileset)
        self.map.set_layer_count(2)
        self.renderer = Renderer(self.tileset, self.map, SCALE)

    def save_map(self, path):
        with open(path, "w") as f:
            data = {
                "layers": self.map.layers,
                "blocked_tiles": list(self.tileset.get_properties(BLOCKED_TILE_TYPE))
            }
            json.dump(data, f, indent=2)

        print(f"Map saved to {path}")

    def load_map(self, path):
        with open(path, "r") as f:
            data = json.load(f)

        self.map.set_layers(data["layers"])
        self.tileset.set_properties({BLOCKED_TILE_TYPE: set(data["blocked_tiles"])})

    def draw_palette(self):
        rows_visible = SCREEN_HEIGHT // self.renderer.render_tile_size
        max_slots = rows_visible * PALETTE_COLS
        drawn_tiles = 0
        for i, tile in enumerate(self.renderer.tiles):
            x = (i % PALETTE_COLS) * self.renderer.render_tile_size
            y = (i // PALETTE_COLS) * self.renderer.render_tile_size
            rotated = pygame.transform.rotate(tile, -90 * self.current_rotation)
            self.screen.blit(rotated, (x, y))
            drawn_tiles += 1

            if self.show_tile_properties and self.tileset.has_property(i, BLOCKED_TILE_TYPE):
                draw_crossed_box(self.screen, x, y, self.renderer.render_tile_size, (0, 150, 255))

            if i == self.selected_tile:
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 0),
                    (x, y, self.renderer.render_tile_size, self.renderer.render_tile_size),
                    2
                )

        for i in range(drawn_tiles, max_slots):
            x = (i % PALETTE_COLS) * self.renderer.render_tile_size
            y = (i // PALETTE_COLS) * self.renderer.render_tile_size
            draw_crossed_box(self.screen, x, y, self.renderer.render_tile_size, (100, 100, 100))

    def draw_map(self):
        def callback(x, y, draw_x, draw_y):
            if not self.show_tile_properties:
                return
            pygame.draw.rect(
                self.screen,
                (60, 60, 60),
                (draw_x, draw_y, self.renderer.render_tile_size, self.renderer.render_tile_size),
                1
            )

        offset = (PALETTE_COLS * self.renderer.render_tile_size, 0)
        self.renderer.render(self.screen, offset, callback)

    def export_map(self, path):
        map_width = MAP_WIDTH * self.renderer.render_tile_size
        map_height = MAP_HEIGHT * self.renderer.render_tile_size
        image = pygame.Surface((map_width, map_height), pygame.SRCALPHA)

        self.renderer.render(image)

        pygame.image.save(image, path)

    def run(self):
        clock = pygame.time.Clock()

        palette_width = PALETTE_COLS * self.renderer.render_tile_size

        running = True
        while running:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_map("map.json")
                    if event.key == pygame.K_l:
                        self.load_map("map.json")
                    if event.key == pygame.K_h:
                        self.show_tile_properties = not self.show_tile_properties
                    if event.key == pygame.K_r:
                        self.current_rotation = (self.current_rotation + 1) % 4
                    if event.key == pygame.K_f:
                        for y in range(MAP_HEIGHT):
                            for x in range(MAP_WIDTH):
                                self.map[self.selected_layer, x, y] = (self.selected_tile, self.current_rotation)
                    if event.key == pygame.K_e:
                        self.export_map("map.png")
                    if event.key == pygame.K_1:
                        self.selected_layer = 0
                    if event.key == pygame.K_2:
                        self.selected_layer = 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if mx < palette_width:
                        col = mx // self.renderer.render_tile_size
                        row = my // self.renderer.render_tile_size
                        index = row * PALETTE_COLS + col
                        if 0 <= index < len(self.renderer.tiles):
                            if event.button == 1:
                                self.selected_tile = index
                            elif event.button == 3:
                                self.tileset.toggle_property(index, BLOCKED_TILE_TYPE)

            mx, my = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            if mouse_buttons[0] or mouse_buttons[2]:
                x = (mx - palette_width) // self.renderer.render_tile_size
                y = my // self.renderer.render_tile_size
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    self.map[self.selected_layer, x, y] = (self.selected_tile if mouse_buttons[0] else 0,
                                                           self.current_rotation)

            self.screen.fill((30, 30, 30))

            self.draw_palette()
            self.draw_map()

            font = pygame.font.SysFont(None, 36)
            label = font.render("H: toggle props | T: load tileset | S/L: save/load", True, (200, 200, 200))
            self.screen.blit(label, (palette_width + 10, SCREEN_HEIGHT - 25))

            pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("Tile Map Editor")

    editor = Editor()
    editor.run()


if __name__ == "__main__":
    main()
