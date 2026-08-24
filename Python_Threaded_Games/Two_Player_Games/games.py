"""
games.py
--------
All multiplayer game logic for the threaded network-games project.

The server imports this file and chooses one of the four games:
    1. Tic-Tac-Toe
    2. Connect Four
    3. Blackjack
    4. Hangman

Each game is designed for exactly two connected players.
The networking itself is handled by server.py.
"""

import random

GAME_NAMES = {
    "1": "Tic-Tac-Toe",
    "2": "Connect Four",
    "3": "Blackjack",
    "4": "Hangman",
}


def _send(send, player, message):
    send(player, message)


def _broadcast(broadcast, message):
    broadcast(message)


# ---------------------------------------------------------------------------
# TIC-TAC-TOE
# ---------------------------------------------------------------------------

def play_tic_tac_toe(players, send, broadcast, receive):
    board = [" "] * 9
    turn = 0

    def board_text():
        cells = [str(i + 1) if board[i] == " " else board[i] for i in range(9)]
        return (
            "\n"
            f" {cells[0]} | {cells[1]} | {cells[2]}\n"
            "---+---+---\n"
            f" {cells[3]} | {cells[4]} | {cells[5]}\n"
            "---+---+---\n"
            f" {cells[6]} | {cells[7]} | {cells[8]}\n"
        )

    def winner(symbol):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        return any(all(board[i] == symbol for i in combo) for combo in wins)

    broadcast("\n===== TIC-TAC-TOE =====")
    broadcast("Player 1 = X | Player 2 = O")
    broadcast(board_text())

    while True:
        symbol = "X" if turn == 0 else "O"
        player = players[turn]

        send(player, "YOUR_TURN")
        send(player, "Choose a position from 1-9. Type QUIT to leave.")

        choice = receive(player).strip()

        if choice.upper() == "QUIT":
            broadcast(f"Player {turn + 1} left. Game ended.")
            return

        try:
            position = int(choice) - 1
        except ValueError:
            send(player, "ERROR: Enter a number from 1-9.")
            continue

        if not 0 <= position < 9:
            send(player, "ERROR: Choose a position from 1-9.")
            continue

        if board[position] != " ":
            send(player, "ERROR: That position is already occupied.")
            continue

        board[position] = symbol
        broadcast(board_text())

        if winner(symbol):
            broadcast(f"Player {turn + 1} ({symbol}) wins!")
            return

        if " " not in board:
            broadcast("Draw!")
            return

        turn = 1 - turn


# ---------------------------------------------------------------------------
# CONNECT FOUR
# ---------------------------------------------------------------------------

def play_connect_four(players, send, broadcast, receive):
    rows, cols = 6, 7
    board = [[" "] * cols for _ in range(rows)]
    turn = 0

    def board_text():
        text = "\n  1   2   3   4   5   6   7\n"
        text += "-----------------------------\n"
        for row in board:
            text += "| " + " | ".join(row) + " |\n"
            text += "-----------------------------\n"
        return text

    def drop(column, piece):
        for row in range(rows - 1, -1, -1):
            if board[row][column] == " ":
                board[row][column] = piece
                return True
        return False

    def winner(piece):
        # Horizontal
        for r in range(rows):
            for c in range(cols - 3):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical
        for r in range(rows - 3):
            for c in range(cols):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True

        # Down-right diagonal
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Up-right diagonal
        for r in range(3, rows):
            for c in range(cols - 3):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def full():
        return all(board[0][c] != " " for c in range(cols))

    broadcast("\n===== CONNECT FOUR =====")
    broadcast("Player 1 = X | Player 2 = O")
    broadcast(board_text())

    while True:
        piece = "X" if turn == 0 else "O"
        player = players[turn]

        send(player, "YOUR_TURN")
        send(player, "Choose a column from 1-7. Type QUIT to leave.")

        choice = receive(player).strip()

        if choice.upper() == "QUIT":
            broadcast(f"Player {turn + 1} left. Game ended.")
            return

        try:
            column = int(choice) - 1
        except ValueError:
            send(player, "ERROR: Enter a column from 1-7.")
            continue

        if not 0 <= column < cols:
            send(player, "ERROR: Choose a column from 1-7.")
            continue

        if not drop(column, piece):
            send(player, "ERROR: That column is full.")
            continue

        broadcast(board_text())

        if winner(piece):
            broadcast(f"Player {turn + 1} ({piece}) wins!")
            return

        if full():
            broadcast("Draw!")
            return

        turn = 1 - turn


# ---------------------------------------------------------------------------
# BLACKJACK
# ---------------------------------------------------------------------------

def play_blackjack(players, send, broadcast, receive):
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
             "J", "Q", "K", "A"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)

    hands = [[], []]
    dealer = [deck.pop(), deck.pop()]

    for player_id in range(2):
        hands[player_id] = [deck.pop(), deck.pop()]

    def card_value(rank):
        if rank in ("J", "Q", "K"):
            return 10
        if rank == "A":
            return 11
        return int(rank)

    def hand_value(hand):
        total = sum(card_value(rank) for rank, _ in hand)
        aces = sum(rank == "A" for rank, _ in hand)

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def hand_text(hand):
        return ", ".join(f"{rank} of {suit}" for rank, suit in hand)

    broadcast("\n===== BLACKJACK =====")
    broadcast("Both players are playing against the dealer.")
    broadcast(
        f"Dealer shows: {dealer[0][0]} of {dealer[0][1]} + hidden card."
    )

    # Each player plays their own hand.
    for player_id in range(2):
        player = players[player_id]

        broadcast(f"Player {player_id + 1}'s turn.")

        while True:
            score = hand_value(hands[player_id])

            send(
                player,
                f"Your hand: {hand_text(hands[player_id])} = {score}"
            )

            if score == 21:
                send(player, "BLACKJACK")
                break

            if score > 21:
                send(player, "BUSTED")
                break

            send(player, "YOUR_TURN")
            send(player, "Type HIT or STAND.")

            choice = receive(player).strip().lower()

            if choice == "quit":
                broadcast(f"Player {player_id + 1} left. Game ended.")
                return

            if choice == "hit":
                card = deck.pop()
                hands[player_id].append(card)
                send(player, f"You drew: {card[0]} of {card[1]}")

                if hand_value(hands[player_id]) > 21:
                    send(player, "You busted.")
                    break

            elif choice == "stand":
                send(player, "You stand.")
                break

            else:
                send(player, "ERROR: Type HIT or STAND.")

    # Dealer plays after both players finish.
    broadcast("\n===== DEALER'S TURN =====")

    while hand_value(dealer) < 17:
        dealer.append(deck.pop())

    dealer_score = hand_value(dealer)
    broadcast(f"Dealer hand: {hand_text(dealer)} = {dealer_score}")

    for player_id in range(2):
        score = hand_value(hands[player_id])

        if score > 21:
            result = "You busted. You lose!"
        elif dealer_score > 21:
            result = "Dealer busted. You win!"
        elif score > dealer_score:
            result = "You win!"
        elif score < dealer_score:
            result = "Dealer wins."
        else:
            result = "Push! It's a draw."

        send(players[player_id], f"Final hand: {hand_text(hands[player_id])}")
        send(players[player_id], f"Final score: {score}")
        send(players[player_id], result)

    broadcast("===== BLACKJACK GAME OVER =====")


# ---------------------------------------------------------------------------
# HANGMAN
# ---------------------------------------------------------------------------

def play_hangman(players, send, broadcast, receive):
    words = [
        "python", "computer", "programming", "developer",
        "software", "keyboard", "internet", "database",
        "network", "college", "student", "technology",
    ]

    word = random.choice(words)
    guessed = set()
    lives = [6, 6]
    turn = 0

    def display():
        return " ".join(
            letter if letter in guessed else "_"
            for letter in word
        )

    broadcast("\n===== HANGMAN =====")
    broadcast("Guess one letter at a time.")
    broadcast(f"Word: {display()}")
    broadcast("Each player starts with 6 lives.")

    while True:
        player = players[turn]

        send(player, "YOUR_TURN")
        send(player, "Enter one letter. Type QUIT to leave.")

        guess = receive(player).strip().lower()

        if guess == "quit":
            broadcast(f"Player {turn + 1} left. Game ended.")
            return

        if len(guess) != 1 or not guess.isalpha():
            send(player, "ERROR: Enter exactly one letter.")
            continue

        if guess in guessed:
            send(player, "ERROR: That letter was already guessed.")
            continue

        guessed.add(guess)

        if guess in word:
            broadcast(f"Player {turn + 1} guessed '{guess}' - correct!")
        else:
            lives[turn] -= 1
            broadcast(
                f"Player {turn + 1} guessed '{guess}' - wrong. "
                f"Lives left: {lives[turn]}"
            )

        broadcast(f"Word: {display()}")

        if all(letter in guessed for letter in word):
            broadcast(f"Player {turn + 1} wins! The word was '{word}'.")
            return

        if lives[0] <= 0 and lives[1] <= 0:
            broadcast(f"Game over! The word was '{word}'.")
            return

        turn = 1 - turn


GAME_FUNCTIONS = {
    "1": play_tic_tac_toe,
    "2": play_connect_four,
    "3": play_blackjack,
    "4": play_hangman,
}


def play_selected_game(game_number, players, send, broadcast, receive):
    """Run the selected game."""
    if game_number not in GAME_FUNCTIONS:
        raise ValueError("Invalid game number.")

    GAME_FUNCTIONS[game_number](
        players,
        send,
        broadcast,
        receive,
    )
