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

    def default_layout():
        pass

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
    a = King('black', 4, 4)
    board.place_figure(a)

    while True:
        move = board.expect_move()
        board.process_move(move)

