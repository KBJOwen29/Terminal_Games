"""
server.py
---------
One server for all four multiplayer games.

Two players connect to this server. After both connect, the server
randomly chooses which player gets to select the game. The selected
player chooses one of the games in games.py, and both players then
play that game.
"""

import random
import socket
import threading

from games import GAME_NAMES, play_selected_game


HOST = "0.0.0.0"
PORT = 5000
MAX_PLAYERS = 2


clients = []
readers = {}
clients_lock = threading.Lock()
send_lock = threading.Lock()


def send(conn, message):
    """Send one newline-terminated message to a client."""
    try:
        with send_lock:
            conn.sendall((message + "\n").encode("utf-8"))
        return True
    except (ConnectionResetError, BrokenPipeError, OSError):
        return False


def broadcast(message):
    """Send a message to both players."""
    with clients_lock:
        current_clients = list(clients)

    for conn in current_clients:
        send(conn, message)


def receive(conn):
    """Read one newline-terminated command from a client."""
    reader = readers[conn]
    line = reader.readline()

    if not line:
        return ""

    return line.strip()


def close_clients():
    with clients_lock:
        current_clients = list(clients)

    for conn in current_clients:
        try:
            readers.get(conn).close()
        except (OSError, AttributeError):
            pass

        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            conn.close()
        except OSError:
            pass


def wait_for_two_players(server):
    """Accept exactly two players."""
    print("Waiting for two players...")

    while len(clients) < MAX_PLAYERS:
        conn, addr = server.accept()

        with clients_lock:
            player_id = len(clients)
            clients.append(conn)
            readers[conn] = conn.makefile("r", encoding="utf-8")

        print(
            f"Player {player_id + 1} connected "
            f"from {addr[0]}:{addr[1]}"
        )

        send(conn, f"PLAYER_ID:{player_id + 1}")
        send(conn, f"Connected as Player {player_id + 1}.")

        if player_id == 0:
            send(conn, "Waiting for Player 2...")
        else:
            send(conn, "Both players are connected!")

    broadcast("READY")
    print("Both players are connected.")


def choose_game():
    """
    Randomly select Player 1 or Player 2 as the game chooser.
    Only that player receives the menu and is allowed to choose.
    """
    chooser = random.randint(0, 1)
    other = 1 - chooser

    broadcast(
        f"CHOOSER:{chooser + 1}"
    )

    send(
        clients[chooser],
        "GAME_CHOOSER"
    )
    send(
        clients[chooser],
        "\nChoose the game you want to play:"
    )

    for number, name in GAME_NAMES.items():
        send(clients[chooser], f"{number}. {name}")

    send(clients[chooser], "GAME_CHOOSER_PROMPT")

    send(
        clients[other],
        f"Player {chooser + 1} was randomly selected "
        "to choose the game."
    )
    send(clients[other], "WAITING_FOR_GAME")

    while True:
        choice = receive(clients[chooser])

        if not choice:
            raise ConnectionError("The game chooser disconnected.")

        if choice in GAME_NAMES:
            return choice, chooser

        send(
            clients[chooser],
            "ERROR: Choose 1, 2, 3, or 4."
        )


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(MAX_PLAYERS)

        print("=" * 50)
        print("MULTIPLAYER NETWORK GAMES SERVER")
        print("=" * 50)
        print(f"Listening on port {PORT}")
        print("Start client.py on both computers.")
        print("Give both players this computer's LAN IP.")
        print()

        wait_for_two_players(server)

        game_number, chooser = choose_game()
        game_name = GAME_NAMES[game_number]

        broadcast(f"GAME_SELECTED:{game_number}")
        broadcast(
            f"Player {chooser + 1} selected {game_name}."
        )

        print(f"Player {chooser + 1} selected {game_name}.")
        print("Starting game...")

        play_selected_game(
            game_number,
            clients,
            send,
            broadcast,
            receive,
        )

        broadcast("SESSION_OVER")
        print("Game session ended.")

    except KeyboardInterrupt:
        print("\nServer stopped by host.")

    except (ConnectionError, OSError) as error:
        print(f"Server error: {error}")

    finally:
        close_clients()
        server.close()
        print("Server closed.")


if __name__ == "__main__":
    main()
