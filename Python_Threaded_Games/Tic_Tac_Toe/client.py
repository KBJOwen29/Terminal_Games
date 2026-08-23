import socket

PORT = 5000

server_ip = input("Enter the host IP address: ").strip()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((server_ip, PORT))

print("\nConnected to Tic-Tac-Toe server.")
print("Enter 1-9 to place your piece. Type QUIT to leave.\n")

while True:
    data = sock.recv(4096).decode()
    if not data:
        break

    print(data, end="")

    if "YOUR_TURN" in data:
        move = input("Your move (1-9): ")
        sock.sendall((move + "\n").encode())

    if "wins!" in data or "Draw!" in data or "Game ended." in data:
        break

sock.close()
