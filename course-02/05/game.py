from blessed import Terminal

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Tile:
    def __init__(self, symbol: str, walkable: bool, pos: Position):
        self.symbol = symbol
        self.walkable = walkable
        self.pos = pos

    def __str__(self):
        return self.symbol


class Empty(Tile):
    def __init__(self, pos):
        super().__init__(" ", True, pos)


class Wall(Tile):
    def __init__(self, pos):
        super().__init__("#", False, pos)


class Treasure(Tile):
    def __init__(self, pos):
        super().__init__("T", True, pos)


class Exit(Tile):
    def __init__(self, pos):
        super().__init__("X", True, pos)


class Entity(Tile):
    def __init__(self, symbol: str, walkable: bool, pos):
        super().__init__(symbol, walkable, pos)

    def move(self):
        pass


class Player(Entity):
    def __init__(self, pos):
        super().__init__("P", True, pos)


class Enemy(Entity):
    def __init__(self, pos):
        super().__init__("E", True, pos)


class Game:
    def __init__(self, width, height, term: Terminal):
        self.width = width
        self.height = height
        self.map = []  # type: list[list[Tile]]
        self.term = term

        for i in range(height):
            tmp = []
            for j in range(width):
                tmp.append(Empty(Position(j, i)))
            self.map.append(tmp)

        self.enemies = []
        self.treasure = None
        self.exit = Exit(Position(width - 2, height - 2))
        self.player = Player(Position(1, 1))

    def _init_map(self):
        pass

    def _place_walls(self):
        pass

    def _place_treasure(self):
        pass

    def _place_enemies(self):
        pass

    def _draw(self):
        pass

    def play(self):
        print(self.term.clear, end="", flush=True)
        text = ""
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                inp = self.term.inkey()
                text += inp
                if inp.code == self.term.KEY_ENTER:
                    text = text[:-1]
                piv = len(text) // 2
                center_term = self.term.move_xy(self.term.width // 2 - piv, self.term.height // 2)
                print(self.term.red_on_green + center_term + text, end="", flush=True)
                if inp == "q":
                    break


def main():
    terminal = Terminal()
    game = Game(10, 10, terminal)
    game.play()


if __name__ == "__main__":
    main()
