import socket
import threading
import random

HOST = "0.0.0.0"
PORT = 5003

WORDS = [
    "python", "computer", "programming", "developer",
    "software", "keyboard", "internet", "database"
]

clients = []
word = random.choice(WORDS)
guessed = set()
lives = [6, 6]
turn = 0
game_over = False
lock = threading.Lock()


def send(c, msg):
    try:
        c.sendall((msg + "\n").encode())
    except:
        pass


def broadcast(msg):
    for c in clients:
        send(c, msg)


def display():
    return " ".join(letter if letter in guessed else "_" for letter in word)


def handle(conn, pid):
    global turn, game_over

    send(conn, f"You are Player {pid + 1}.")
    while len(clients) < 2:
        threading.Event().wait(0.1)

    if pid == 0:
        broadcast(f"\nWord: {display()}")
        broadcast("Players take turns guessing letters.")

    while not game_over:
        if turn != pid:
            send(conn, "WAIT")
            threading.Event().wait(0.2)
            continue

        send(conn, "YOUR_TURN")
        data = conn.recv(1024).decode().strip().lower()

        if data == "quit":
            broadcast("A player left. Game ended.")
            game_over = True
            return

        if len(data) != 1 or not data.isalpha():
            send(conn, "Enter one letter.")
            continue

        if data in guessed:
            send(conn, "That letter was already guessed.")
            continue

        guessed.add(data)

        if data not in word:
            lives[pid] -= 1
            broadcast(f"Player {pid + 1} guessed '{data}' - wrong. Lives: {lives[pid]}")
        else:
            broadcast(f"Player {pid + 1} guessed '{data}' - correct!")

        broadcast(f"Word: {display()}")

        if all(c in guessed for c in word):
            broadcast(f"Player {pid + 1} wins! The word was '{word}'.")
            game_over = True
            break

        if lives[0] <= 0 and lives[1] <= 0:
            broadcast(f"Game over! The word was '{word}'.")
            game_over = True
            break

        turn = 1 - turn


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)

    print(f"Hangman server running on port {PORT}.")
    print(f"Secret word: {word} (host testing only)")

    while len(clients) < 2:
        conn, addr = server.accept()
        clients.append(conn)
        pid = len(clients) - 1
        print(f"Player {pid + 1} connected from {addr}")
        threading.Thread(target=handle, args=(conn, pid), daemon=True).start()

    while not game_over:
        threading.Event().wait(1)


if __name__ == "__main__":
    main()
