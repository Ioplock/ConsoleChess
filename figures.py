from itertools import chain

class Figure:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.offsets = None # Offsets format {"white": [(..., ...), (...., ...., check), ...], ..., }
        # check is needed for "special" moves

    def get_valid_moves(self, board):
        moves = []
        if self.offsets is None:
            return ('any')
        for offset in self.offsets[board.get_curr_color()]["default"]:
            cords = (self.x + offset[0], self.y + offset[1])
            if board.is_is_in_bounds(cords[0], cords[1]) or (len(offset) == 3 and offset[2]()):
                dest = board.get_figure(cords[0], cords[1])
                if dest is None or dest.color != self.color:
                    moves.append(cords)
        return moves

    def is_valid_move(self, new_x, new_y, board):
        if board.turn and self.color == 'white':
            return False
        moves = self.get_valid_moves(board)
        if (new_x, new_y) in moves or 'any' in moves:
            return True
            

    def make_move(self, new_x, new_y, board):
        board.remove_figure(self.x, self.y)
        self.x = new_x
        self.y = new_y
        return board.place_figure(self)

    def __str__(self) -> str:
        return self.type[0].upper() if self.color == 'white' else self.type[0].lower()
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, (Figure, str)):
            return str(self) == str(value)
        else:
            return False

class Pawn(Figure):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'pawn'
        self.is_first_move_double = False
        self.offsets = {"white": [(0, -1), (0, -2, lambda: self.y == 6)], "black": [(0, 1), (0, 2, lambda: self.y == 1)]}

class Knight(Figure):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'knight'
        offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        self.offsets = {"white": offsets, "black": offsets}

class Rook(Figure):
    offsets = list(chain.from_iterable([[(0, i), (i, 0), (-i, 0), (0, -i)] for i in range(8)]))

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'rook'
        self.offsets = {"white": Rook.offsets, "black": Rook.offsets}

class Bishop(Figure):
    offsets = list(chain.from_iterable([[(-i, -i),(i, i),(-i, i),(i, -i)] for i in range(8)]))

    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'bishop'
        self.offsets = {"white": Bishop.offsets, "black": Bishop.offsets}

class Queen(Figure):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'queen'
        offsets = Rook.offsets + Bishop.offsets
        self.offsets = {"white": offsets, "black": offsets}

class King(Figure):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'king'
        offsets = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.offsets = {"white": offsets, "black": offsets}