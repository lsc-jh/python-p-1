import asyncio
import pygame
from network import NetworkClient
from lib import GameMap, Camera, draw_ui, draw_players, draw_bullets, PLAYER_SIZE

SERVER_HOST = "kou-gen.net"
SERVER_PORT = 8080

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


async def main():
    pygame.init()

    network = NetworkClient(SERVER_HOST, SERVER_PORT)
    await network.connect()

    asyncio.create_task(network.listen())

    game_map = GameMap(network.map_data)

    screen_width = min(SCREEN_WIDTH, game_map.width_px)
    screen_height = min(SCREEN_HEIGHT, game_map.height_px)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Multiplayer Shooter")

    game_map.load()

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 32)

    camera = Camera(screen_width, screen_height, game_map.width_px, game_map.height_px)

    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        world_mouse_x, world_mouse_y = camera.screen_to_world(mouse_x, mouse_y)

        mouse_buttons = pygame.mouse.get_pressed()

        input_state = {
            "up": keys[pygame.K_w],
            "down": keys[pygame.K_s],
            "left": keys[pygame.K_a],
            "right": keys[pygame.K_d],
            "shoot": mouse_buttons[0] or keys[pygame.K_SPACE],
            "mouse_x": world_mouse_x,
            "mouse_y": world_mouse_y,
        }

        await network.send_input(input_state)

        state = network.state

        screen.fill((0, 0, 0))

        if state is not None:
            players = state["players"]
            bullets = state["bullets"]

            my_player = players.get(network.player_id)

            if my_player is not None:
                camera.follow_position(
                    my_player["x"] + PLAYER_SIZE / 2,
                    my_player["y"] + PLAYER_SIZE / 2,
                )

            game_map.draw(screen, camera)
            draw_bullets(screen, bullets, camera)
            draw_players(screen, players, camera, network.player_id)
            draw_ui(screen, font, my_player)

        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
