from figures import * 

class Move:
    def __init__(self, xy1, xy2, fig, dest):  # xy(1-2) tuples of cords
        self.xy1 = xy1
        self.xy2 = xy2
        self.fig = fig
        self.dest = dest

    def __str__(self) -> str:
        return f"{self.fig} from {self.xy1} to {self.xy2}"

class Board:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.allowed_nums = "12345678"
        self.allowed_letters = "abcdefgh"
        self.turn = True
        self.moves = []
        self.get_curr_color = lambda: 'white' if self.turn else 'black'

    def default_layout(self):
        figures = [
            Rook('black', 0, 0),
            Knight('black', 1, 0),
            Bishop('black', 2, 0),
            King('black', 3, 0),
            Queen('black', 4, 0),
            Bishop('black', 5, 0),
            Knight('black', 6, 0),
            Rook('black', 7, 0),
            Rook('white', 0, 7),
            Knight('white', 1, 7),
            Bishop('white', 2, 7),
            King('white', 3, 7),
            Queen('white', 4, 7),
            Bishop('white', 5, 7),
            Knight('white', 6, 7),
            Rook('white', 7, 7)
        ]
        for i in range(8):
            figures.append(Pawn('black', i, 1))
            figures.append(Pawn('white', i, 6))
        self.__batch_place_figure(figures)

    def checkers_layout(self):
        figures = [
            Checker('black', 0, 1),
            Checker('black', 1, 0),
            Checker('black', 1, 2),
            Checker('black', 2, 1),
            Checker('black', 3, 0),
            Checker('black', 3, 2),
            Checker('black', 4, 1),
            Checker('black', 5, 0),
            Checker('black', 5, 2),
            Checker('black', 6, 1),
            Checker('black', 7, 0),
            Checker('black', 7, 2),

            Checker('white', 0, 5),
            Checker('white', 0, 7),
            Checker('white', 1, 6),
            Checker('white', 2, 5),
            Checker('white', 2, 7),
            Checker('white', 3, 6),
            Checker('white', 4, 5),
            Checker('white', 4, 7),
            Checker('white', 5, 6),
            Checker('white', 6, 5),
            Checker('white', 6, 7),
            Checker('white', 7, 6),
        ]
        self.__batch_place_figure(figures)

    def process_move(self, move):
        print(move)
        fig = move.fig.make_move(move.xy2[0], move.xy2[1], self)
        print(fig)

    def __parse_num_cord(self, cord):
        if len(cord) != 2 or str(cord[0]).lower() not in self.allowed_letters or cord[1] not in self.allowed_nums:
            return None
        return (self.allowed_letters.index(str(cord[0]).lower()), 8 - int(cord[1]))

    def __input_cords(self):
        xy = None
        while not xy:
            xy = input(f"Enter the coordinates of the {self.get_curr_color()} figure in format - [Letter Digit]: ")
            if xy == "exit":
                exit(-1)
            xy = self.__parse_num_cord(xy)
            if not xy:
                print("Invalid coordinates")
                continue
        return xy


    def expect_move(self):
        self.print_board()
        xy1, xy2 = None, None
        reset = lambda: (None, None)
        while not xy1 and not xy2:
            xy1, xy2 = self.__input_cords(), self.__input_cords()
            fig = self.get_figure(xy1[0], xy1[1])
            if str(fig) == ".":
                print("Can't move blank place!")
                xy1, xy2 = reset()
                continue
            if not self.turn and str(fig).isupper() or self.turn and str(fig).islower():
                print(f"It's {self.get_curr_color()} turn!")
                xy1, xy2 = reset()
                continue
            if not fig.is_valid_move(xy2[0], xy2[1], self):
                print("This figure can't move there!")
                xy1, xy2 = reset()
                continue
        
        move = Move(xy1, xy2, fig, board.get_figure(xy2[0], xy2[1]))
        self.turn = not self.turn
        return move

    def get_figure(self, x, y):
        if self.is_in_bounds(x, y):
            return self.board[y][x]
        else:
            return None

    def __batch_place_figure(self, figures):
        for fig in figures:
            self.place_figure(fig)

    def place_figure(self, figure):
        if self.is_in_bounds(figure.x, figure.y):
            if self.is_empty(figure.x, figure.y):
                self.board[figure.y][figure.x] = figure
                return None
            else:
                tfig = self.remove_figure(figure.x, figure.y)
                self.board[figure.y][figure.x] = figure
                return tfig
        else:
            raise Exception("Invalid move")

    def remove_figure(self, x, y):
        if self.is_in_bounds(x, y):
            if self.is_empty(x, y):
                raise Exception("Invalid move")
            else:
                tfig = self.get_figure(x, y)
                self.board[y][x] = '.'
                return tfig
        else:
            raise Exception("Invalid move")

    def is_empty(self, x, y):
        if self.is_in_bounds(x, y):
            return self.board[y][x] == '.'
        else:
            raise Exception("Invalid cords")

    def is_in_bounds(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def print_board(self):
        print("   A B C D E F G H   ")
        for y in range(len(self.board)):
            print(f"{8 - y}  ", end='')
            for x in range(len(self.board[y])):
                print(str(self.board[y][x])[0], end=' ')
            print(f" {8 - y}")
        print("   A B C D E F G H   ")
    
if __name__ == "__main__":
    board = Board()
    # board.default_layout()
    board.checkers_layout()

    while True:
        move = board.expect_move()
        board.process_move(move)