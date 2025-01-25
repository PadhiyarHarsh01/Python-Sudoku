import random

class SudokuGame:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        self.notes = [[set() for _ in range(9)] for _ in range(9)]

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

        # Store the original board for reference
        for i in range(9):
            for j in range(9):
                self.original_board[i][j] = self.board[i][j]

    def is_complete(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def make_move(self, row, col, num):
        if self.original_board[row][col] == 0:  # Only allow changes to empty cells
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num
                self.notes[row][col].clear()  # Clear notes when making a move
                return True
        return False

    def clear_move(self, row, col):
        if self.original_board[row][col] == 0:  # Only allow clearing of non-original cells
            self.board[row][col] = 0
            return True
        return False

    def toggle_note(self, row, col, num):
        if self.original_board[row][col] == 0 and self.board[row][col] == 0:
            if num in self.notes[row][col]:
                self.notes[row][col].remove(num)
            else:
                self.notes[row][col].add(num)
            return True
        return False

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0 or not self.is_valid(self.board[i][j], (i, j)):
                    return False
        return True

