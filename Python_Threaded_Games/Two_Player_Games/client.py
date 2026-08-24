"""
client.py
---------
One client for all four multiplayer games.

The client connects to server.py. The server randomly decides which
player gets to choose the game. The client then displays the messages
from the server and sends input whenever it receives YOUR_TURN or
GAME_CHOOSER.
"""

import socket


PORT = 5000


def receive(reader):
    """Read one newline-terminated server message."""
    line = reader.readline()
    if not line:
        return ""
    return line.rstrip("\n")


def main():
    server_ip = input("Enter the host/server IP address: ").strip()

    if not server_ip:
        print("Server IP cannot be empty.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((server_ip, PORT))
    except OSError as error:
        print(f"Could not connect to server: {error}")
        return

    print("\nConnected to the Multiplayer Network Games server.")
    print("Waiting for another player...\n")

    reader = sock.makefile("r", encoding="utf-8")

    try:
        while True:
            message = receive(reader)

            if not message:
                print("\nServer disconnected.")
                break

            # Internal status messages are handled without printing
            # their raw protocol name.
            if message.startswith("PLAYER_ID:"):
                player_id = message.split(":", 1)[1]
                print(f"You are Player {player_id}.")
                continue

            if message == "READY":
                print("Both players are connected!")
                continue

            if message == "GAME_CHOOSER":
                print("\n*** YOU WERE RANDOMLY CHOSEN TO PICK THE GAME ***")
                continue

            if message == "WAITING_FOR_GAME":
                print("Waiting for the other player to choose a game...")
                continue

            if message.startswith("CHOOSER:"):
                chooser = message.split(":", 1)[1]
                print(
                    f"Player {chooser} was randomly selected "
                    "to choose the game."
                )
                continue

            if message.startswith("GAME_SELECTED:"):
                continue

            if message == "SESSION_OVER":
                print("\nThe game session is over.")
                break

            print(message)

            # Game-selection input.
            if message == "GAME_CHOOSER":
                continue

            if message == "GAME_CHOOSER_PROMPT":
                choice = input("Enter your choice (1-4): ").strip()
                sock.sendall((choice + "\n").encode("utf-8"))
                continue

            # The server sends the menu as separate messages. The
            # actual prompt is recognized by the text below.
            if message == "4. Hangman":
                # Do not automatically input here. The menu is followed
                # by GAME_SELECTION_PROMPT from the server in future
                # versions; currently selection is triggered by the
                # protocol marker below.
                pass

            if message == "YOUR_TURN":
                choice = input("> ").strip()
                sock.sendall((choice + "\n").encode("utf-8"))


    except (ConnectionResetError, BrokenPipeError, OSError) as error:
        print(f"\nConnection error: {error}")

    finally:
        try:
            reader.close()
        except (OSError, UnboundLocalError):
            pass
        try:
            sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
