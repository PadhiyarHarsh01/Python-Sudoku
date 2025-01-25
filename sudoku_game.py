import random

class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def print_board(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, num, pos):
        # Check row
        for j in range(9):
            if self.board[pos[0]][j] == num and pos[1] != j:
                return False

        # Check column
        for i in range(9):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True
        else:
            row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num

                if self.solve():
                    return True

                self.board[row][col] = 0

        return False

    def generate_puzzle(self, difficulty):
        self.solve()
        cells_to_remove = 40 + (9 - difficulty) * 5  # Adjust difficulty (1-9)

        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_to_remove -= 1

    def is_complete(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def make_move(self, row, col, num):
        if self.board[row][col] == 0:
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                return True
        return False

def play_sudoku():
    game = SudokuGame()
    print("Welcome to Sudoku!")
    difficulty = int(input("Enter difficulty level (1-9, where 9 is the easiest): "))
    game.generate_puzzle(difficulty)

    while not game.is_complete():
        game.print_board()
        print("\nEnter your move (row column number) or 'q' to quit:")
        move = input().strip().lower()
        
        if move == 'q':
            print("Thanks for playing!")
            return

        try:
            row, col, num = map(int, move.split())
            if 1 <= row <= 9 and 1 <= col <= 9 and 1 <= num <= 9:
                if game.make_move(row - 1, col - 1, num):
                    print("Valid move!")
                else:
                    print("Invalid move. Try again.")
            else:
                print("Invalid input. Row, column, and number should be between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter three numbers separated by spaces.")

    print("Congratulations! You've solved the Sudoku puzzle!")
    game.print_board()

if __name__ == "__main__":
    play_sudoku()

# Test the Sudoku solver
test_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

print("Testing Sudoku solver:")
test_game = SudokuGame()
test_game.board = test_board
print("Initial board:")
test_game.print_board()
print("\nSolved board:")
test_game.solve()
test_game.print_board()

print("\nStarting interactive Sudoku game:")
play_sudoku()

