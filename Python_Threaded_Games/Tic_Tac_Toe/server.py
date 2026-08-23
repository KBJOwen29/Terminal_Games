import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = []
lock = threading.Lock()

board = [" "] * 9
turn = 0
game_over = False


def send(player, message):
    try:
        player.sendall((message + "\n").encode())
    except:
        pass


def broadcast(message):
    with lock:
        for player in clients:
            send(player, message)


def board_text():
    return (
        f"\n {board[0]} | {board[1]} | {board[2]} "
        "\n---+---+---"
        f"\n {board[3]} | {board[4]} | {board[5]} "
        "\n---+---+---"
        f"\n {board[6]} | {board[7]} | {board[8]} "
        "\n"
    )


def winner(player):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(all(board[i] == player for i in combo) for combo in wins)


def reset():
    global board, turn, game_over
    board = [" "] * 9
    turn = 0
    game_over = False


def handle_client(conn, player_id):
    global turn, game_over

    symbol = "X" if player_id == 0 else "O"
    send(conn, f"You are Player {symbol}.")
    send(conn, "Waiting for the other player..." if len(clients) < 2 else "Game ready.")

    while len(clients) < 2:
        pass

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

        if not data:
            return

        if data.upper() == "QUIT":
            broadcast(f"Player {symbol} disconnected. Game ended.")
            game_over = True
            return

        try:
            pos = int(data) - 1
        except ValueError:
            send(conn, "Invalid move. Enter 1-9.")
            continue

        if not 0 <= pos < 9 or board[pos] != " ":
            send(conn, "Invalid move. Choose an empty position from 1-9.")
            continue

        board[pos] = symbol
        broadcast(board_text())

        if winner(symbol):
            broadcast(f"Player {symbol} wins!")
            game_over = True
            break

        if " " not in board:
            broadcast("Draw!")
            game_over = True
            break

        turn = 1 - turn


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2)

    print(f"Tic-Tac-Toe server running on port {PORT}.")
    print("Give the other player this computer's LAN IP address.")

    while len(clients) < 2:
        conn, addr = server.accept()
        with lock:
            clients.append(conn)
            player_id = len(clients) - 1
        print(f"Player {player_id + 1} connected from {addr}")
        threading.Thread(target=handle_client, args=(conn, player_id), daemon=True).start()

    print("Two players connected. Game started.")
    while not game_over:
        threading.Event().wait(1)


if __name__ == "__main__":
    main()
