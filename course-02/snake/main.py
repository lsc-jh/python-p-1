import random
from collections import deque
import os
from blessed import Terminal

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
        self.direction = (0, 0)
        self.pending_direction = self.direction
        self.food = None
        self.game_over = False

    def reset(self):
        start_x = WIDTH // 2
        start_y = HEIGHT // 2

        self.snake = deque()
        self.snake.appendleft((start_x, start_y))
        self.snake.appendleft((start_x - 1, start_y))
        self.snake.appendleft((start_x - 2, start_y))

        self.direction = (-1, 0)
        self.pending_direction = self.direction

        self.food = random_empty_cell(self.snake)

        self.game_over = False

    def set_direction(self, move):
        move = move.lower()
        if move == "w":
            new_dir = (0, -1)
        elif move == "s":
            new_dir = (0, 1)
        elif move == "a":
            new_dir = (-1, 0)
        elif move == "d":
            new_dir = (1, 0)
        else:
            new_dir = self.direction

        dx, dy = self.direction
        ndx, ndy = new_dir
        if (dx, dy) == (-ndx, -ndy):
            return

        self.pending_direction = new_dir

    def apply_direction(self):
        self.direction = self.pending_direction

    def update(self):
        self.apply_direction()
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_x = head_x + dx
        new_y = head_y + dy
        new_head = (new_x, new_y)

        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.appendleft(new_head)

        if new_head == self.food:
            self.food = random_empty_cell(self.snake)
        else:
            self.snake.pop()

    def draw(self):
        clear_screen()

        grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

        fx, fy = self.food
        grid[fy][fx] = FOOD

        for i, (x, y) in enumerate(self.snake):
            if i == 0:
                grid[y][x] = SNAKE_HEAD
            else:
                grid[y][x] = SNAKE_BODY

        for row in grid:
            print(" ".join(row))

        print()
        print("Use W/A/S/D | Q to quit")

    def run(self):
        term = Terminal()
        with term.fullscreen(), term.cbreak(), term.hidden_cursor():
            while True:
                self.draw()

                if self.game_over:
                    choice = input("Game Over! Play again? (y/n): ").lower()
                    if choice == "y":
                        self.reset()
                        continue
                    else:
                        break

                key = term.inkey(timeout=0.1).lower()
                if key == "q":
                    break
                self.set_direction(key)
                self.update()


if __name__ == "__main__":
    game = SnakeGame()
    game.reset()
    game.run()
