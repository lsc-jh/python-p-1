import random
from collections import deque
import os

WIDTH = 15
HEIGHT = 10

EMPTY = "."
SNAKE_HEAD = "O"
SNAKE_BODY = "o"
FOOD = "*"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def random_empty_cell(snake_positions):
    while True:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if (x, y) not in snake_positions:
            return (x, y)


class SnakeGame:
    def __init__(self):
        self.snake = deque()

    def reset(self):
        start_x = WIDTH // 2
        start_y = HEIGHT // 2

        self.snake = deque()
        self.snake.appendleft((start_x, start_y))
        self.snake.appendleft((start_x - 1, start_y))
        self.snake.appendleft((start_x - 2, start_y))

    def draw(self):
        clear_screen()

        grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                grid[y][x] = SNAKE_HEAD
            else:
                grid[y][x] = SNAKE_BODY

        for row in grid:
            print(" ".join(row))

        print()
        print("Use W/A/S/D | Q to quit")


if __name__ == "__main__":
    game = SnakeGame()
    game.reset()
    game.draw()
