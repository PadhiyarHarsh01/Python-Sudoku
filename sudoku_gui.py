import pygame
import sys
from sudoku_logic import SudokuGame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
FONT_SIZE = 32

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)
small_font = pygame.font.Font(None, FONT_SIZE // 2)
note_font = pygame.font.Font(None, FONT_SIZE // 3)

def draw_grid():
    for i in range(GRID_SIZE + 1):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - 60), thickness)

def draw_numbers(game):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if game.board[i][j] != 0:
                color = BLACK if game.original_board[i][j] != 0 else LIGHT_BLUE
                number = font.render(str(game.board[i][j]), True, color)
                x = j * CELL_SIZE + CELL_SIZE // 2 - number.get_width() // 2
                y = i * CELL_SIZE + CELL_SIZE // 2 - number.get_height() // 2
                screen.blit(number, (x, y))
            elif game.notes[i][j]:
                for num in range(1, 10):
                    if num in game.notes[i][j]:
                        note = note_font.render(str(num), True, GRAY)
                        x = j * CELL_SIZE + ((num - 1) % 3) * (CELL_SIZE // 3) + 5
                        y = i * CELL_SIZE + ((num - 1) // 3) * (CELL_SIZE // 3) + 5
                        screen.blit(note, (x, y))

def draw_selected_cell(row, col):
    pygame.draw.rect(screen, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def draw_buttons():
    solve_button = pygame.draw.rect(screen, GRAY, (10, HEIGHT - 50, 100, 40))
    solve_text = small_font.render("Solve", True, BLACK)
    screen.blit(solve_text, (35, HEIGHT - 40))

    reset_button = pygame.draw.rect(screen, GRAY, (120, HEIGHT - 50, 100, 40))
    reset_text = small_font.render("Reset", True, BLACK)
    screen.blit(reset_text, (145, HEIGHT - 40))

    check_button = pygame.draw.rect(screen, GRAY, (230, HEIGHT - 50, 100, 40))
    check_text = small_font.render("Check", True, BLACK)
    screen.blit(check_text, (255, HEIGHT - 40))

    return solve_button, reset_button, check_button

def main():
    game = SudokuGame()
    game.generate_puzzle(5)  # Adjust difficulty here (1-9)

    selected_cell = None
    solved = False
    note_mode = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < HEIGHT - 60:
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    selected_cell = (row, col)
                else:
                    if solve_button.collidepoint(x, y) and not solved:
                        game.solve()
                        solved = True
                    elif reset_button.collidepoint(x, y):
                        game = SudokuGame()
                        game.generate_puzzle(5)  # Adjust difficulty here (1-9)
                        solved = False
                        selected_cell = None
                    elif check_button.collidepoint(x, y):
                        if game.check_solution():
                            print("Correct solution!")
                        else:
                            print("Incorrect solution. Keep trying!")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    note_mode = not note_mode
                elif selected_cell and not solved:
                    row, col = selected_cell
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        game.clear_move(row, col)
                    elif event.unicode.isdigit() and event.unicode != '0':
                        num = int(event.unicode)
                        if note_mode:
                            game.toggle_note(row, col, num)
                        else:
                            game.make_move(row, col, num)

        screen.fill(WHITE)
        draw_grid()
        draw_numbers(game)
        if selected_cell:
            draw_selected_cell(*selected_cell)

        solve_button, reset_button, check_button = draw_buttons()

        # Display note mode status
        note_status = small_font.render(f"Note Mode: {'ON' if note_mode else 'OFF'}", True, BLACK)
        screen.blit(note_status, (WIDTH - 120, HEIGHT - 40))

        pygame.display.flip()

if __name__ == "__main__":
    main()

