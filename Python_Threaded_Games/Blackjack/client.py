import socket

PORT = 5002
ip = input("Enter the host IP address: ").strip()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, PORT))

print("\nConnected to multiplayer Blackjack.")
print("Commands: hit / stand\n")

while True:
    data = sock.recv(8192).decode()
    if not data:
        break

    print(data, end="")

    if "YOUR_TURN" in data:
        choice = input("Choose hit or stand: ").strip().lower()
        sock.sendall((choice + "\n").encode())

    if "You wins!" in data or "You loses." in data or "You busted." in data or "pushes" in data:
        # The server may send the result after the dealer resolves.
        pass

sock.close()
