import socket

PORT = 5001
ip = input("Enter the host IP address: ").strip()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, PORT))

print("\nConnected to Connect Four.")
print("Choose columns 1-7.\n")

while True:
    data = sock.recv(8192).decode()
    if not data:
        break

    print(data, end="")

    if "YOUR_TURN" in data:
        move = input("Your column (1-7): ")
        sock.sendall((move + "\n").encode())

    if "wins!" in data or "Draw!" in data or "Game ended." in data:
        break

sock.close()
