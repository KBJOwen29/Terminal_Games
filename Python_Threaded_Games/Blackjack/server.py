import socket
import threading
import random

HOST = "0.0.0.0"
PORT = 5002

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]

clients = []
hands = [[], []]
deck = []
dealer = []
turn = 0
game_started = False
game_finished = False
finished_players = 0

finished_event = threading.Event()
lock = threading.Lock()


def send(conn, message):
    try:
        conn.sendall((message + "\n").encode())
    except:
        pass


def broadcast(message):
    for conn in clients:
        send(conn, message)


def create_deck():
    cards = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(cards)
    return cards


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


def player_thread(conn, player_id):
    global turn, finished_players

    send(conn, f"You are Player {player_id + 1}.")
    send(conn, "Waiting for the second player...")

    while len(clients) < 2:
        threading.Event().wait(0.1)

    while not game_started:
        threading.Event().wait(0.1)

    send(
        conn,
        f"Your hand: {hand_text(hands[player_id])} "
        f"= {hand_value(hands[player_id])}"
    )

    while True:
        if game_finished:
            break

        if turn != player_id:
            threading.Event().wait(0.1)
            continue

        if hand_value(hands[player_id]) >= 21:
            with lock:
                turn = 1 - turn
                finished_players += 1
            break

        send(conn, "YOUR_TURN")

        try:
            choice = conn.recv(1024).decode().strip().lower()
        except:
            return

        if choice == "hit":
            hands[player_id].append(deck.pop())

            send(
                conn,
                f"You drew: {hands[player_id][-1][0]} of "
                f"{hands[player_id][-1][1]}"
            )
            send(
                conn,
                f"Your hand: {hand_text(hands[player_id])} "
                f"= {hand_value(hands[player_id])}"
            )

            if hand_value(hands[player_id]) >= 21:
                with lock:
                    turn = 1 - turn
                    finished_players += 1
                break

        elif choice == "stand":
            with lock:
                turn = 1 - turn
                finished_players += 1
            break

        else:
            send(conn, "Invalid choice. Type hit or stand.")

    send(conn, "Your turn is finished. Waiting for the dealer...")


def main():
    global deck, dealer, game_started, game_finished, turn

    deck = create_deck()
    dealer = [deck.pop(), deck.pop()]
    hands[0] = [deck.pop(), deck.pop()]
    hands[1] = [deck.pop(), deck.pop()]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)

    print(f"Blackjack server running on port {PORT}.")
    print("The host computer should also run client.py.")
    print("Share the host computer's LAN IP with the guest.")

    while len(clients) < 2:
        conn, addr = server.accept()
        clients.append(conn)
        player_id = len(clients) - 1

        print(f"Player {player_id + 1} connected from {addr}")

        threading.Thread(
            target=player_thread,
            args=(conn, player_id),
            daemon=True
        ).start()

    game_started = True
    broadcast("\n===== BLACKJACK START =====")
    broadcast("Both players are playing against the dealer.")
    broadcast(f"Dealer shows: {dealer[0][0]} of {dealer[0][1]} + hidden card.")

    turn = 0

    while finished_players < 2:
        threading.Event().wait(0.1)

    broadcast("\n===== DEALER'S TURN =====")

    while hand_value(dealer) < 17:
        dealer.append(deck.pop())

    dealer_score = hand_value(dealer)

    broadcast(f"Dealer hand: {hand_text(dealer)} = {dealer_score}")

    for player_id in range(2):
        player_score = hand_value(hands[player_id])

        if player_score > 21:
            result = "You busted. You lose!"
        elif dealer_score > 21:
            result = "Dealer busted. You win!"
        elif player_score > dealer_score:
            result = "You win!"
        elif player_score < dealer_score:
            result = "Dealer wins."
        else:
            result = "Push! It's a draw."

        send(clients[player_id], f"Final hand: {hand_text(hands[player_id])}")
        send(clients[player_id], f"Final score: {player_score}")
        send(clients[player_id], result)

    game_finished = True
    finished_event.set()

    print("Game finished.")
    server.close()


if __name__ == "__main__":
    main()
