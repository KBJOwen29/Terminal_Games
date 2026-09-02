# ==========================================
# PYTHON CHESS GAME
# ==========================================
# Two-player terminal chess
#
# White pieces: uppercase
# Black pieces: lowercase
#
# Input example:
# e2 e4
# g8 f6
#
# Type "quit" to exit.
# ==========================================


# ------------------------------------------
# CREATE BOARD
# ------------------------------------------

board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]


# ------------------------------------------
# GAME VARIABLES
# ------------------------------------------

turn = "white"

white_castle_kingside = True
white_castle_queenside = True
black_castle_kingside = True
black_castle_queenside = True

en_passant = None

game_over = False


# ------------------------------------------
# DISPLAY BOARD
# ------------------------------------------

def display_board():
    print()
    print("    a   b   c   d   e   f   g   h")
    print("  +---+---+---+---+---+---+---+---+")

    row = 0

    while row < 8:
        print(str(8 - row) + " |", end=" ")

        col = 0

        while col < 8:
            print(board[row][col] + " |", end=" ")
            col += 1

        print(" " + str(8 - row))
        print("  +---+---+---+---+---+---+---+---+")

        row += 1

    print("    a   b   c   d   e   f   g   h")
    print()


# ------------------------------------------
# CONVERT CHESS POSITION
# ------------------------------------------

def position_to_coordinates(position):

    if len(position) != 2:
        return None

    file = position[0]
    rank = position[1]

    if file == "a":
        col = 0
    elif file == "b":
        col = 1
    elif file == "c":
        col = 2
    elif file == "d":
        col = 3
    elif file == "e":
        col = 4
    elif file == "f":
        col = 5
    elif file == "g":
        col = 6
    elif file == "h":
        col = 7
    else:
        return None

    if rank == "1":
        row = 7
    elif rank == "2":
        row = 6
    elif rank == "3":
        row = 5
    elif rank == "4":
        row = 4
    elif rank == "5":
        row = 3
    elif rank == "6":
        row = 2
    elif rank == "7":
        row = 1
    elif rank == "8":
        row = 0
    else:
        return None

    return [row, col]


# ------------------------------------------
# CHECK IF POSITION IS ON BOARD
# ------------------------------------------

def is_inside(row, col):

    if row >= 0 and row < 8 and col >= 0 and col < 8:
        return True
    else:
        return False


# ------------------------------------------
# CHECK PIECE COLOR
# ------------------------------------------

def is_white(piece):

    if piece >= "A" and piece <= "Z":
        return True
    else:
        return False


def is_black(piece):

    if piece >= "a" and piece <= "z":
        return True
    else:
        return False


# ------------------------------------------
# CHECK IF PIECE BELONGS TO PLAYER
# ------------------------------------------

def belongs_to_player(piece, player):

    if piece == " ":
        return False

    if player == "white":

        if is_white(piece):
            return True
        else:
            return False

    elif player == "black":

        if is_black(piece):
            return True
        else:
            return False

    else:
        return False


# ------------------------------------------
# CHECK IF PIECE IS ENEMY
# ------------------------------------------

def is_enemy(piece, player):

    if piece == " ":
        return False

    if player == "white":

        if is_black(piece):
            return True
        else:
            return False

    elif player == "black":

        if is_white(piece):
            return True
        else:
            return False

    else:
        return False


# ------------------------------------------
# CHECK PATH FOR ROOK/BISHOP/QUEEN
# ------------------------------------------

def path_is_clear(start_row, start_col, end_row, end_col):

    row_change = 0
    col_change = 0

    if end_row > start_row:
        row_change = 1
    elif end_row < start_row:
        row_change = -1
    else:
        row_change = 0

    if end_col > start_col:
        col_change = 1
    elif end_col < start_col:
        col_change = -1
    else:
        col_change = 0

    row = start_row + row_change
    col = start_col + col_change

    while row != end_row or col != end_col:

        if board[row][col] != " ":
            return False

        row += row_change
        col += col_change

    return True


# ------------------------------------------
# FIND KING
# ------------------------------------------

def find_king(player):

    row = 0

    while row < 8:

        col = 0

        while col < 8:

            piece = board[row][col]

            if player == "white":

                if piece == "K":
                    return [row, col]

            elif player == "black":

                if piece == "k":
                    return [row, col]

            col += 1

        row += 1

    return None


# ------------------------------------------
# CHECK IF A SQUARE IS ATTACKED
# ------------------------------------------

def square_is_attacked(row, col, attacker):

    r = 0

    while r < 8:

        c = 0

        while c < 8:

            piece = board[r][c]

            if belongs_to_player(piece, attacker):

                target_row = row
                target_col = col

                row_difference = target_row - r
                col_difference = target_col - c

                # ----------------------------------
                # PAWN
                # ----------------------------------

                if piece == "P":

                    if row_difference == -1:
                        if col_difference == 1 or col_difference == -1:
                            return True

                elif piece == "p":

                    if row_difference == 1:
                        if col_difference == 1 or col_difference == -1:
                            return True

                # ----------------------------------
                # KNIGHT
                # ----------------------------------

                elif piece == "N" or piece == "n":

                    if abs(row_difference) == 2 and abs(col_difference) == 1:
                        return True

                    elif abs(row_difference) == 1 and abs(col_difference) == 2:
                        return True

                # ----------------------------------
                # KING
                # ----------------------------------

                elif piece == "K" or piece == "k":

                    if abs(row_difference) <= 1 and abs(col_difference) <= 1:
                        return True

                # ----------------------------------
                # ROOK
                # ----------------------------------

                elif piece == "R" or piece == "r":

                    if r == target_row or c == target_col:

                        if path_is_clear(r, c, target_row, target_col):
                            return True

                # ----------------------------------
                # BISHOP
                # ----------------------------------

                elif piece == "B" or piece == "b":

                    if abs(row_difference) == abs(col_difference):

                        if path_is_clear(r, c, target_row, target_col):
                            return True

                # ----------------------------------
                # QUEEN
                # ----------------------------------

                elif piece == "Q" or piece == "q":

                    if r == target_row or c == target_col:

                        if path_is_clear(r, c, target_row, target_col):
                            return True

                    elif abs(row_difference) == abs(col_difference):

                        if path_is_clear(r, c, target_row, target_col):
                            return True

            c += 1

        r += 1

    return False


# ------------------------------------------
# CHECK IF PLAYER IS IN CHECK
# ------------------------------------------

def is_in_check(player):

    king = find_king(player)

    if king is None:
        return True

    if player == "white":
        enemy = "black"
    else:
        enemy = "white"

    if square_is_attacked(king[0], king[1], enemy):
        return True
    else:
        return False


# ------------------------------------------
# BASIC MOVE VALIDATION
# ------------------------------------------

def valid_piece_move(start_row, start_col, end_row, end_col, player):

    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    if not belongs_to_player(piece, player):
        return False

    if target != " ":

        if belongs_to_player(target, player):
            return False

        if target == "K" or target == "k":
            return False

    row_difference = end_row - start_row
    col_difference = end_col - start_col

    abs_row = abs(row_difference)
    abs_col = abs(col_difference)

    # --------------------------------------
    # PAWN
    # --------------------------------------

    if piece == "P":

        # Normal move
        if col_difference == 0 and row_difference == -1:

            if target == " ":
                return True

        # First double move
        elif col_difference == 0 and row_difference == -2:

            if start_row == 6:

                if board[start_row - 1][start_col] == " ":
                    if target == " ":
                        return True

        # Capture
        elif abs(col_difference) == 1 and row_difference == -1:

            if is_enemy(target, player):
                return True

    elif piece == "p":

        # Normal move
        if col_difference == 0 and row_difference == 1:

            if target == " ":
                return True

        # First double move
        elif col_difference == 0 and row_difference == 2:

            if start_row == 1:

                if board[start_row + 1][start_col] == " ":
                    if target == " ":
                        return True

        # Capture
        elif abs(col_difference) == 1 and row_difference == 1:

            if is_enemy(target, player):
                return True

    # --------------------------------------
    # KNIGHT
    # --------------------------------------

    elif piece == "N" or piece == "n":

        if abs_row == 2 and abs_col == 1:
            return True

        elif abs_row == 1 and abs_col == 2:
            return True

    # --------------------------------------
    # ROOK
    # --------------------------------------

    elif piece == "R" or piece == "r":

        if row_difference == 0 or col_difference == 0:

            if path_is_clear(start_row, start_col, end_row, end_col):
                return True

    # --------------------------------------
    # BISHOP
    # --------------------------------------

    elif piece == "B" or piece == "b":

        if abs_row == abs_col:

            if path_is_clear(start_row, start_col, end_row, end_col):
                return True

    # --------------------------------------
    # QUEEN
    # --------------------------------------

    elif piece == "Q" or piece == "q":

        if row_difference == 0 or col_difference == 0:

            if path_is_clear(start_row, start_col, end_row, end_col):
                return True

        elif abs_row == abs_col:

            if path_is_clear(start_row, start_col, end_row, end_col):
                return True

    # --------------------------------------
    # KING
    # --------------------------------------

    elif piece == "K" or piece == "k":

        if abs_row <= 1 and abs_col <= 1:

            if abs_row != 0 or abs_col != 0:
                return True

    return False


# ------------------------------------------
# CASTLING VALIDATION
# ------------------------------------------

def valid_castle(start_row, start_col, end_row, end_col, player):

    if player == "white":

        # White kingside
        if start_row == 7 and start_col == 4:
            if end_row == 7 and end_col == 6:

                if white_castle_kingside:

                    if board[7][5] == " " and board[7][6] == " ":

                        if board[7][7] == "R":

                            if not is_in_check("white"):

                                if not square_is_attacked(7, 5, "black"):

                                    if not square_is_attacked(7, 6, "black"):
                                        return True

            # White queenside
            if end_row == 7 and end_col == 2:

                if white_castle_queenside:

                    if board[7][1] == " ":
                        if board[7][2] == " ":
                            if board[7][3] == " ":

                                if board[7][0] == "R":

                                    if not is_in_check("white"):

                                        if not square_is_attacked(7, 3, "black"):

                                            if not square_is_attacked(7, 2, "black"):
                                                return True

    elif player == "black":

        # Black kingside
        if start_row == 0 and start_col == 4:
            if end_row == 0 and end_col == 6:

                if black_castle_kingside:

                    if board[0][5] == " " and board[0][6] == " ":

                        if board[0][7] == "r":

                            if not is_in_check("black"):

                                if not square_is_attacked(0, 5, "white"):

                                    if not square_is_attacked(0, 6, "white"):
                                        return True

            # Black queenside
            if end_row == 0 and end_col == 2:

                if black_castle_queenside:

                    if board[0][1] == " ":
                        if board[0][2] == " ":
                            if board[0][3] == " ":

                                if board[0][0] == "r":

                                    if not is_in_check("black"):

                                        if not square_is_attacked(0, 3, "white"):

                                            if not square_is_attacked(0, 2, "white"):
                                                return True

    return False


# ------------------------------------------
# MAKE TEMPORARY MOVE
# ------------------------------------------

def make_move(start_row, start_col, end_row, end_col):

    captured = board[end_row][end_col]

    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = " "

    return captured


# ------------------------------------------
# UNDO MOVE
# ------------------------------------------

def undo_move(start_row, start_col, end_row, end_col, captured):

    board[start_row][start_col] = board[end_row][end_col]
    board[end_row][end_col] = captured


# ------------------------------------------
# CHECK IF MOVE LEAVES PLAYER IN CHECK
# ------------------------------------------

def move_leaves_check(start_row, start_col, end_row, end_col, player):

    captured = board[end_row][end_col]

    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = " "

    result = is_in_check(player)

    board[start_row][start_col] = board[end_row][end_col]
    board[end_row][end_col] = captured

    return result


# ------------------------------------------
# EN PASSANT VALIDATION
# ------------------------------------------

def valid_en_passant(start_row, start_col, end_row, end_col, player):

    if en_passant is None:
        return False

    if end_row != en_passant[0]:
        return False

    if end_col != en_passant[1]:
        return False

    piece = board[start_row][start_col]

    if player == "white":

        if piece == "P":

            if start_row == 3:

                if abs(start_col - end_col) == 1:
                    return True

    elif player == "black":

        if piece == "p":

            if start_row == 4:

                if abs(start_col - end_col) == 1:
                    return True

    return False


# ------------------------------------------
# CHECK LEGAL MOVE
# ------------------------------------------

def legal_move(start_row, start_col, end_row, end_col, player):

    if not is_inside(start_row, start_col):
        return False

    if not is_inside(end_row, end_col):
        return False

    piece = board[start_row][start_col]

    if not belongs_to_player(piece, player):
        return False

    # Castling
    if piece == "K" or piece == "k":

        if abs(end_col - start_col) == 2:

            if valid_castle(start_row, start_col, end_row, end_col, player):
                return True
            else:
                return False

    # Normal movement
    if valid_piece_move(start_row, start_col, end_row, end_col, player):

        if not move_leaves_check(start_row, start_col, end_row, end_col, player):
            return True

    # En passant
    if valid_en_passant(start_row, start_col, end_row, end_col, player):

        captured_row = start_row
        captured_col = end_col

        captured_piece = board[captured_row][captured_col]

        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = " "
        board[captured_row][captured_col] = " "

        check = is_in_check(player)

        board[start_row][start_col] = board[end_row][end_col]
        board[end_row][end_col] = " "
        board[captured_row][captured_col] = captured_piece

        if not check:
            return True

    return False


# ------------------------------------------
# CHECK IF PLAYER HAS ANY LEGAL MOVE
# ------------------------------------------

def has_legal_moves(player):

    start_row = 0

    while start_row < 8:

        start_col = 0

        while start_col < 8:

            if belongs_to_player(board[start_row][start_col], player):

                end_row = 0

                while end_row < 8:

                    end_col = 0

                    while end_col < 8:

                        if legal_move(
                            start_row,
                            start_col,
                            end_row,
                            end_col,
                            player
                        ):
                            return True

                        end_col += 1

                    end_row += 1

            start_col += 1

        start_row += 1

    return False


# ------------------------------------------
# PROMOTION
# ------------------------------------------

def promote_pawn(row, col):

    piece = board[row][col]

    if piece == "P":

        print("White pawn promotion.")
        print("Choose Q = Queen")
        print("Choose R = Rook")
        print("Choose B = Bishop")
        print("Choose N = Knight")

        choice = input("Promotion: ").upper()

        if choice == "Q":
            board[row][col] = "Q"

        elif choice == "R":
            board[row][col] = "R"

        elif choice == "B":
            board[row][col] = "B"

        elif choice == "N":
            board[row][col] = "N"

        else:
            board[row][col] = "Q"

    elif piece == "p":

        print("Black pawn promotion.")
        print("Choose Q = Queen")
        print("Choose R = Rook")
        print("Choose B = Bishop")
        print("Choose N = Knight")

        choice = input("Promotion: ").lower()

        if choice == "q":
            board[row][col] = "q"

        elif choice == "r":
            board[row][col] = "r"

        elif choice == "b":
            board[row][col] = "b"

        elif choice == "n":
            board[row][col] = "n"

        else:
            board[row][col] = "q"


# ------------------------------------------
# UPDATE CASTLING RIGHTS
# ------------------------------------------

def update_castling_rights(
    piece,
    start_row,
    start_col,
    end_row,
    end_col,
    captured
):

    global white_castle_kingside
    global white_castle_queenside
    global black_castle_kingside
    global black_castle_queenside

    # White king moved
    if piece == "K":

        white_castle_kingside = False
        white_castle_queenside = False

    # Black king moved
    elif piece == "k":

        black_castle_kingside = False
        black_castle_queenside = False

    # White rook moved
    elif piece == "R":

        if start_row == 7 and start_col == 0:
            white_castle_queenside = False

        elif start_row == 7 and start_col == 7:
            white_castle_kingside = False

    # Black rook moved
    elif piece == "r":

        if start_row == 0 and start_col == 0:
            black_castle_queenside = False

        elif start_row == 0 and start_col == 7:
            black_castle_kingside = False

    # White rook captured
    if captured == "R":

        if end_row == 7 and end_col == 0:
            white_castle_queenside = False

        elif end_row == 7 and end_col == 7:
            white_castle_kingside = False

    # Black rook captured
    elif captured == "r":

        if end_row == 0 and end_col == 0:
            black_castle_queenside = False

        elif end_row == 0 and end_col == 7:
            black_castle_kingside = False


# ------------------------------------------
# EXECUTE CASTLING
# ------------------------------------------

def execute_castle(start_row, start_col, end_row, end_col):

    king = board[start_row][start_col]

    board[start_row][start_col] = " "
    board[end_row][end_col] = king

    # Kingside
    if end_col == 6:

        rook = board[start_row][7]

        board[start_row][7] = " "
        board[start_row][5] = rook

    # Queenside
    elif end_col == 2:

        rook = board[start_row][0]

        board[start_row][0] = " "
        board[start_row][3] = rook


# ------------------------------------------
# EXECUTE EN PASSANT
# ------------------------------------------

def execute_en_passant(start_row, start_col, end_row, end_col):

    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = " "

    captured_row = start_row
    captured_col = end_col

    board[captured_row][captured_col] = " "


# ------------------------------------------
# MAKE FULL MOVE
# ------------------------------------------

def execute_move(start_row, start_col, end_row, end_col, player):

    global en_passant

    piece = board[start_row][start_col]

    captured = board[end_row][end_col]

    update_castling_rights(
        piece,
        start_row,
        start_col,
        end_row,
        end_col,
        captured
    )

    # Reset en passant
    old_en_passant = en_passant
    en_passant = None

    # Castling
    if piece == "K" or piece == "k":

        if abs(end_col - start_col) == 2:

            execute_castle(
                start_row,
                start_col,
                end_row,
                end_col
            )

            return

    # En passant
    if valid_en_passant(
        start_row,
        start_col,
        end_row,
        end_col,
        player
    ):

        execute_en_passant(
            start_row,
            start_col,
            end_row,
            end_col
        )

        return

    # Normal move
    board[end_row][end_col] = piece
    board[start_row][start_col] = " "

    # Set new en passant square
    if piece == "P":

        if start_row == 6 and end_row == 4:

            en_passant = [5, start_col]

    elif piece == "p":

        if start_row == 1 and end_row == 3:

            en_passant = [2, start_col]

    # Promotion
    if piece == "P":

        if end_row == 0:
            promote_pawn(end_row, end_col)

    elif piece == "p":

        if end_row == 7:
            promote_pawn(end_row, end_col)


# ------------------------------------------
# GAME LOOP
# ------------------------------------------

print()
print("==========================================")
print("           PYTHON CHESS GAME")
print("==========================================")
print()
print("White pieces are uppercase.")
print("Black pieces are lowercase.")
print()
print("Enter moves like:")
print("e2 e4")
print("g8 f6")
print()
print("Type quit to exit.")
print()

while game_over == False:

    display_board()

    # --------------------------------------
    # CHECK CURRENT PLAYER
    # --------------------------------------

    if is_in_check(turn):

        print(turn.capitalize() + " is in CHECK!")

    # --------------------------------------
    # CHECKMATE / STALEMATE
    # --------------------------------------

    if not has_legal_moves(turn):

        if is_in_check(turn):

            if turn == "white":
                print("CHECKMATE!")
                print("Black wins!")

            elif turn == "black":
                print("CHECKMATE!")
                print("White wins!")

        else:

            print("STALEMATE!")
            print("The game is a draw.")

        game_over = True

        continue

    # --------------------------------------
    # ASK FOR MOVE
    # --------------------------------------

    print(turn.capitalize() + "'s turn.")

    move = input("Move: ").lower().strip()

    if move == "quit":
        print("Game ended.")
        game_over = True
        continue

    parts = move.split()

    if len(parts) != 2:

        print("Invalid input.")
        print("Use: e2 e4")
        continue

    start = position_to_coordinates(parts[0])
    end = position_to_coordinates(parts[1])

    if start is None or end is None:

        print("Invalid board position.")
        continue

    start_row = start[0]
    start_col = start[1]

    end_row = end[0]
    end_col = end[1]

    piece = board[start_row][start_col]

    # --------------------------------------
    # CHECK IF MOVE IS LEGAL
    # --------------------------------------

    if legal_move(
        start_row,
        start_col,
        end_row,
        end_col,
        turn
    ):

        execute_move(
            start_row,
            start_col,
            end_row,
            end_col,
            turn
        )

        # Change player
        if turn == "white":
            turn = "black"

        elif turn == "black":
            turn = "white"

    else:

        print("Illegal move.")
        print("Try another move.")