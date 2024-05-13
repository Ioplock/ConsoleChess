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
        for offset in self.offsets[board.get_curr_color()]:
            cords = (self.x + offset[0], self.y + offset[1])
            if board.is_in_bounds(cords[0], cords[1]):
                dest = board.get_figure(cords[0], cords[1])
                if len(offset) == 3:
                    if offset[2](**{"fig": dest, "board": board, "offset": offset}):
                        moves.append(cords)
                        continue
                    else:
                        continue
                if dest is None or dest == '.' or dest.color != self.color:
                    moves.append(cords)
        return moves

    def is_valid_move(self, new_x, new_y, board):
        if (not board.turn and self.color == 'white') or (board.turn and self.color == 'black'):
            return False
        moves = self.get_valid_moves(board)
        print(moves)
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
        self.offsets = {"white": [(0, -1), (0, -2, self.__if_first), (1, -1, self.__can_eat), (-1, -1, self.__can_eat)], "black": [(0, 1), (0, 2, self.__if_first), (1, 1, self.__can_eat), (-1, 1, self.__can_eat)]}

    def __if_first(self, **kwargs):
        print(self.y)
        if self.color == 'white':
            return self.y == 6
        else:
            return self.y == 1
        
    def __can_eat(self, **kwargs):
        assert kwargs["fig"]
        if kwargs["fig"] != '.' and kwargs["fig"].color != self.color:
            print("wtf")
            return True
        else:
            return False


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

class Checker(Figure):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.type = 'checker'
        offsets = [(2, 2, self.__can_move), (-2, 2, self.__can_move), (2, -2, self.__can_move), (-2, -2, self.__can_move)]
        self.offsets = {"white": offsets + [(-1,-1, self.__have_to_eat), (1, -1, self.__have_to_eat)], "black": offsets + [(-1,-1, self.__have_to_eat), (1, -1, self.__have_to_eat)]}

    def __have_to_eat(self, **kwargs):  # Inverted for better usability
        assert kwargs["board"]
        assert kwargs["fig"]
        offesets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for offset in offesets:
            if kwargs["board"].is_in_bounds(self.x + offset[0], self.y + offset[1]):
                dest = kwargs["board"].get_figure(self.x + offset[0], self.y + offset[1])
                if dest != '.' and dest.color != self.color:
                    print("Cannot go there, have to eat the piece")
                    return False
        return kwargs["fig"] == '.'

    def __can_move(self, **kwargs):
        assert kwargs["board"]
        assert kwargs["offset"]
        in_mid_fig = kwargs["board"].get_figure(int(self.x + kwargs["offset"][0] * 0.5), int(self.y + kwargs["offset"][1] * 0.5))
        if in_mid_fig == '.':
            return False
        return in_mid_fig.color!= self.color
