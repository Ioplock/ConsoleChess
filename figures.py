class Figure:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.offsets = None # Offsets format {"white": {"default": [(..., ...), (..., ...), ..., ], "special": [(..., ..., check), ..., ]}, ..., }

    def get_valid_moves(self, board): # TODO: add check for special moves and reformat code
        moves = []
        if self.offsets is None:
            return ('any')
        for offset in self.offsets[board.get_curr_color()]:
            cords = (self.x + offset[0], self.y + offset[1])
            if board.is_is_in_bounds(cords[0], cords[1]):
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
    
class King(Figure):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'king'

    # def is_valid_move(self, new_x, new_y, board):
    #     return True

class Pawn(Figure):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'pawn'
        self.is_first_move_double = True
        self.offsets = {"white": [(0, -1), (0, -2)], "black": [(0, 1), (0, 2)]}

    def is_valid_move(self, new_x, new_y, board):
        if not super.is_valid_move(new_x, new_y, board):
            return False
        