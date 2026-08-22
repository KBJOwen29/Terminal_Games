ROWS = 6
COLUMNS = 7

board = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def display_board():
    print("\n  1   2   3   4   5   6   7")
    print("-----------------------------")

    for row in board:
        print("| " + " | ".join(row) + " |")
        print("-----------------------------")


def drop_piece(column, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == " ":
            board[row][column] = player
            return True

    return False


def check_winner(player):
    # Horizontal
    for row in range(ROWS):
        for column in range(COLUMNS - 3):
            if (
                board[row][column] == player
                and board[row][column + 1] == player
                and board[row][column + 2] == player
                and board[row][column + 3] == player
            ):
                return True

    # Vertical
    for row in range(ROWS - 3):
        for column in range(COLUMNS):
            if (
                board[row][column] == player
                and board[row + 1][column] == player
                and board[row + 2][column] == player
                and board[row + 3][column] == player
            ):
                return True

    # Diagonal - top left to bottom right
    for row in range(ROWS - 3):
        for column in range(COLUMNS - 3):
            if (
                board[row][column] == player
                and board[row + 1][column + 1] == player
                and board[row + 2][column + 2] == player
                and board[row + 3][column + 3] == player
            ):
                return True

    # Diagonal - bottom left to top right
    for row in range(3, ROWS):
        for column in range(COLUMNS - 3):
            if (
                board[row][column] == player
                and board[row - 1][column + 1] == player
                and board[row - 2][column + 2] == player
                and board[row - 3][column + 3] == player
            ):
                return True

    return False


def board_full():
    for column in range(COLUMNS):
        if board[0][column] == " ":
            return False

    return True


def play_game():
    current_player = "X"

    print("===== CONNECT FOUR =====")
    print("Player X and Player O")
    print("Connect four pieces to win!")

    while True:
        display_board()

        print(f"\nPlayer {current_player}'s turn.")

        try:
            column = int(input("Choose a column (1-7): ")) - 1
        except ValueError:
            print("Please enter a number from 1 to 7.")
            continue

        if column < 0 or column >= COLUMNS:
            print("Invalid column.")
            continue

        if not drop_piece(column, current_player):
            print("That column is full.")
            continue

        if check_winner(current_player):
            display_board()
            print(f"\n🎉 Player {current_player} wins!")
            break

        if board_full():
            display_board()
            print("\nIt's a draw!")
            break

        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


def main():
    while True:
        play_game()

        choice = input("\nPlay again? (Y/N): ").lower()

        if choice != "y":
            print("Thanks for playing!")
            break


main()
