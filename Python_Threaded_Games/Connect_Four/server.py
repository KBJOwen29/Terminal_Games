import socket
import threading

HOST = "0.0.0.0"
PORT = 5001
ROWS, COLS = 6, 7

clients = []
lock = threading.Lock()
board = [[" "] * COLS for _ in range(ROWS)]
turn = 0
game_over = False


def send(conn, msg):
    try:
        conn.sendall((msg + "\n").encode())
    except:
        pass


def broadcast(msg):
    with lock:
        for c in clients:
            send(c, msg)


def board_text():
    s = "\n  1   2   3   4   5   6   7\n"
    s += "-----------------------------\n"
    for row in board:
        s += "| " + " | ".join(row) + " |\n"
        s += "-----------------------------\n"
    return s


def drop(col, piece):
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = piece
            return True
    return False


def winner(piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False


def full():
    return all(board[0][c] != " " for c in range(COLS))


def handle(conn, player_id):
    global turn, game_over

    piece = "X" if player_id == 0 else "O"
    send(conn, f"You are Player {piece}.")
    send(conn, "Waiting for Player 2..." if len(clients) < 2 else "Game ready.")

    while len(clients) < 2:
        threading.Event().wait(0.1)

    if player_id == 0:
        broadcast(board_text())
        broadcast("Player X goes first.")

    while not game_over:
        if turn != player_id:
            send(conn, "WAIT")
            threading.Event().wait(0.2)
            continue

        send(conn, "YOUR_TURN")
        try:
            data = conn.recv(1024).decode().strip()
        except:
            return

        if data.upper() == "QUIT":
            broadcast(f"Player {piece} disconnected. Game ended.")
            game_over = True
            return

        try:
            col = int(data) - 1
        except ValueError:
            send(conn, "Enter a column from 1-7.")
            continue

        if not 0 <= col < COLS:
            send(conn, "Invalid column.")
            continue

        if not drop(col, piece):
            send(conn, "That column is full.")
            continue

        broadcast(board_text())

        if winner(piece):
            broadcast(f"Player {piece} wins!")
            game_over = True
            break

        if full():
            broadcast("Draw!")
            game_over = True
            break

        turn = 1 - turn


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)

    print(f"Connect Four server running on port {PORT}.")
    print("Share the host computer's LAN IP with the guest.")

    while len(clients) < 2:
        conn, addr = server.accept()
        with lock:
            clients.append(conn)
            pid = len(clients) - 1
        print(f"Player {pid + 1} connected from {addr}")
        threading.Thread(target=handle, args=(conn, pid), daemon=True).start()

    while not game_over:
        threading.Event().wait(1)


if __name__ == "__main__":
    main()
