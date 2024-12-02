import random
import os

# Function to display the game board
def print_board(board):
    """
    Clears the screen and prints the game board with centered numbers.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Clear screen
    print("\n2048 Game\n")
    for row in board:
        print("+------+------+------+------+")  # Top border of each row
        for cell in row:
            # Print each cell centered in a 6-character width
            print(f"|{cell:^6}" if cell != 0 else "|      ", end="")
        print("|")  # End of row
    print("+------+------+------+------+")  # Bottom border of the board

# Function to add a new tile (2 or 4) to an empty spot on the board
def add_new_tile(board):
    """
    Randomly selects an empty cell and assigns it a 2 (90% chance) or 4 (10% chance).
    """
    empty_cells = [(r, c) for r in range(4) for c in range(4) if board[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        board[r][c] = 2 if random.random() < 0.9 else 4

# Function to compress the board by moving all non-zero tiles to the left
def compress(board):
    """
    Shifts all numbers in each row to the left, filling with zeros.
    """
    new_board = [[0] * 4 for _ in range(4)]
    for r in range(4):
        pos = 0
        for c in range(4):
            if board[r][c] != 0:
                new_board[r][pos] = board[r][c]
                pos += 1
    return new_board

# Function to merge tiles in each row if they are the same
def merge(board):
    """
    Combines adjacent tiles of the same value and doubles the left tile's value.
    """
    for r in range(4):
        for c in range(3):  # Only check up to the third column
            if board[r][c] == board[r][c + 1] and board[r][c] != 0:
                board[r][c] *= 2  # Double the value
                board[r][c + 1] = 0  # Set the merged tile to zero
    return board

# Function to reverse the rows of the board (used for right moves)
def reverse(board):
    """
    Reverses each row of the board.
    """
    return [row[::-1] for row in board]

# Function to transpose the board (used for up and down moves)
def transpose(board):
    """
    Converts rows to columns and vice versa.
    """
    return [list(row) for row in zip(*board)]

# Functions to handle moves in each direction
def move_left(board):
    """
    Executes a left move: compress, merge, and compress again.
    """
    board = compress(board)
    board = merge(board)
    board = compress(board)
    return board

def move_right(board):
    """
    Executes a right move: reverse, move left, and reverse back.
    """
    board = reverse(board)
    board = move_left(board)
    board = reverse(board)
    return board

def move_up(board):
    """
    Executes an up move: transpose, move left, and transpose back.
    """
    board = transpose(board)
    board = move_left(board)
    board = transpose(board)
    return board

def move_down(board):
    """
    Executes a down move: transpose, move right, and transpose back.
    """
    board = transpose(board)
    board = move_right(board)
    board = transpose(board)
    return board

# Function to check if there are no more valid moves
def check_game_over(board):
    """
    Checks if the game is over (no empty cells and no adjacent tiles with the same value).
    """
    for r in range(4):
        for c in range(4):
            if board[r][c] == 0:  # Empty cell found
                return False
            if c < 3 and board[r][c] == board[r][c + 1]:  # Horizontal merge possible
                return False
            if r < 3 and board[r][c] == board[r + 1][c]:  # Vertical merge possible
                return False
    return True

# Main game loop
def main():
    """
    Initializes the game board and handles user inputs to play the game.
    """
    # Initialize the board with zeros and add two tiles
    board = [[0] * 4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)

    # Game loop
    while True:
        print_board(board)  # Display the board
        if check_game_over(board):  # Check if the game is over
            print("Game Over! No moves left.")
            break

        # Get user input for the move
        move = input("Enter move (W=Up, S=Down, A=Left, D=Right): ").lower()
        if move not in ["w", "a", "s", "d"]:  # Validate input
            print("Invalid input! Use W, A, S, D.")
            continue

        # Make the move
        if move == "w":
            new_board = move_up(board)
        elif move == "s":
            new_board = move_down(board)
        elif move == "a":
            new_board = move_left(board)
        elif move == "d":
            new_board = move_right(board)

        # If the board changes, add a new tile
        if new_board != board:
            board = new_board
            add_new_tile(board)

if __name__ == "__main__":
    main()
