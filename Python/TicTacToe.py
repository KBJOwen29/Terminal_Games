board = [" " for _ in range(9)]


def display_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def check_winner(player):
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for combination in winning_combinations:
        if all(board[position] == player for position in combination):
            return True

    return False


def check_draw():
    return " " not in board


def play_game():
    current_player = "X"

    while True:
        display_board()

        print(f"Player {current_player}'s turn.")

        try:
            position = int(input("Choose a position (1-9): ")) - 1

            if position < 0 or position > 8:
                print("Please choose a number from 1 to 9.")
                continue

            if board[position] != " ":
                print("That position is already occupied.")
                continue

            board[position] = current_player

        except ValueError:
            print("Please enter a valid number.")
            continue

        if check_winner(current_player):
            display_board()
            print(f"Player {current_player} wins!")
            break

        if check_draw():
            display_board()
            print("It's a draw!")
            break

        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


print("===== TIC-TAC-TOE =====")
print("Positions:")
print()
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 ")

play_game()
