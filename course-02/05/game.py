import os
import platform
import subprocess
import random
from blessed import Terminal


def execute():
    script_dir = os.path.abspath(os.path.dirname(__file__))

    if platform.system() == "Windows":
        ps1_path = os.path.join(script_dir, "run.ps1")
        subprocess.run([
            "powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", ps1_path
        ])
    elif platform.system() == "Darwin":
        sh_path = os.path.join(script_dir, "run.sh")

        subprocess.run([
            "osascript", "-e",
            f'''
                 tell application "iTerm"
                     create window with default profile
                     tell current session of current window
                        write text "bash '{sh_path}'"
                     end tell
                 end tell
                 '''
        ])
    else:
        print("Unsupported OS")


HORIZONTAL_WALL = "══"
TOP_LEFT_CORNER = "╔═"
TOP_RIGHT_CORNER = "═╗"
VERTICAL_WALL = "║"
BOTTOM_LEFT_CORNER = "╚═"
BOTTOM_RIGHT_CORNER = "═╝"

BLOCK = "█"


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tile:

    def __init__(self, symbol: str, walkable: bool, pos: Position, term: Terminal):
        self.term = term
        self.symbol = symbol
        self.walkable = walkable
        self.pos = pos
        print(self, end="", flush=True)

    def _render(self, color=None, custom_symbol=None):
        color = color or self.term.white
        custom_symbol = custom_symbol or self.symbol
        return self.term.move_xy(self.pos.x * 2, self.pos.y) + color(custom_symbol) + self.term.normal

    def __str__(self):
        return self._render()


class Entity(Tile):

    def __init__(self, symbol: str, walkable: bool, pos: Position, term: Terminal):
        super().__init__(symbol, walkable, pos, term)

    def move(self, dx, dy, board: list[list[Tile]]):
        pass


class Wall(Tile):

    def __init__(self, pos, term: Terminal, map_size: tuple[int, int], is_pretty=False):
        self.map_size = map_size
        self.is_pretty = is_pretty
        super().__init__("▒▒", False, pos, term)

    def _render(self, color=None, custom_symbol=None):
        return super()._render(color=self.term.ivory4, custom_symbol=custom_symbol)

    def __str__(self):
        if not self.is_pretty:
            if self.pos.y == 0 or self.pos.y == self.map_size[1] - 1:
                return self._render(custom_symbol=BLOCK * 2)
            if self.pos.x == 0 or self.pos.x == self.map_size[0] - 1:
                return self._render(custom_symbol=BLOCK * 2)
        if self.pos.x == 0 and self.pos.y == 0:
            return self._render(custom_symbol=TOP_LEFT_CORNER)
        if self.pos.x == self.map_size[0] - 1 and self.pos.y == 0:
            return self._render(custom_symbol=TOP_RIGHT_CORNER)
        if self.pos.x == 0 and self.pos.y == self.map_size[1] - 1:
            return self._render(custom_symbol=BOTTOM_LEFT_CORNER)
        if self.pos.x == self.map_size[0] - 1 and self.pos.y == self.map_size[1] - 1:
            return self._render(custom_symbol=BOTTOM_RIGHT_CORNER)
        if self.pos.x == 0:
            return self._render(custom_symbol=VERTICAL_WALL)
        if self.pos.x == self.map_size[0] - 1:
            return self._render(custom_symbol=" " + VERTICAL_WALL)
        if self.pos.y == 0 or self.pos.y == self.map_size[1] - 1:
            return self._render(custom_symbol=HORIZONTAL_WALL)

        return super().__str__()


class Empty(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__("  ", True, pos, term)


class Treasure(Tile):

    def __init__(self, pos, term: Terminal):
        self.collected = False
        super().__init__(BLOCK * 2, True, pos, term)

    def __str__(self):
        color = self.term.gold if self.collected else self.term.sienna4
        return self._render(color=color)

    def collect(self):
        self.collected = True


class Exit(Tile):

    def __init__(self, pos, term: Terminal):
        super().__init__("XX", True, pos, term)


class Player(Entity):

    def __init__(self, pos, term: Terminal):
        super().__init__(BLOCK * 2, True, pos, term)

    def move(self, dx, dy, board: list[list[Tile]]):
        x, y = self.pos.x + dx, self.pos.y + dy
        tile = board[y][x]
        if tile.walkable:
            board[self.pos.y][self.pos.x] = Empty(self.pos, self.term)
            self.pos = Position(x, y)
            if isinstance(tile, Treasure):
                tile.collect()


class Enemy(Entity):

    def __init__(self, pos, term: Terminal):
        super().__init__("EE", True, pos, term)


class Game:
    def __init__(self, width, height, term: Terminal):
        self.width = width
        self.height = height
        self.map = []  # type: list[list[Tile]]
        self.term = term

        for i in range(height):
            tmp = []
            for j in range(width):
                tmp.append(Empty(Position(j, i), self.term))
            self.map.append(tmp)

        self.enemies = []
        self.treasure = None
        self.exit = Exit(Position(width - 2, height - 2), self.term)
        self.player = Player(Position(1, 1), self.term)
        self._init_map()

    def _init_map(self):
        self._place_walls()

    def _place_walls(self):
        for i in range(self.height):
            self.map[i][0] = Wall(Position(0, i), self.term, (self.width, self.height))

    def _place_treasure(self):
        pass

    def _place_enemies(self):
        pass

    def _draw(self):
        if self.treasure is not None:
            print(self.treasure)
        print(self.player)

    def play(self):
        print(self.term.home + self.term.clear, end="", flush=True)
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                self._draw()
                inp = self.term.inkey()
                if inp == "q":
                    break
                elif inp in ["w", "W"]:
                    self.player.move(0, -1, self.map)
                elif inp in ["s", "S"]:
                    self.player.move(0, 1, self.map)
                elif inp in ["a", "A"]:
                    self.player.move(-1, 0, self.map)
                elif inp in ["d", "D"]:
                    self.player.move(1, 0, self.map)


def main():
    terminal = Terminal()
    game = Game(10, 10, terminal)
    game.play()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
