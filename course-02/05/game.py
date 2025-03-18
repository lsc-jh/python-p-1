import curses

class Tile:
    def __init__(self, symbol: str, walkable: bool):
        self.symbol = symbol
        self.walkable = walkable

    def __str__(self):
        return self.symbol


class Wall(Tile):
    def __init__(self):
        super().__init__("#", False)


class Treasure(Tile):
    def __init__(self):
        super().__init__("T", True)


class Exit(Tile):
    def __init__(self):
        super().__init__("X", True)


class Entity(Tile):
    def __init__(self, symbol: str, walkable: bool):
        super().__init__(symbol, walkable)

    def move(self):
        pass


class Player(Entity):
    def __init__(self):
        super().__init__("P", True)



class Enemy(Entity):
    def __init__(self):
        super().__init__("E", True)