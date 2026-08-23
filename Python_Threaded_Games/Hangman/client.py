import socket

PORT = 5003
ip = input("Enter the host IP address: ").strip()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, PORT))

print("\nConnected to multiplayer Hangman.")
print("Guess one letter at a time.\n")

while True:
    data = sock.recv(8192).decode()
    if not data:
        break

    print(data, end="")

    if "YOUR_TURN" in data:
        guess = input("Your letter: ").strip()
        sock.sendall((guess + "\n").encode())

    if "wins!" in data or "Game over!" in data or "Game ended." in data:
        break

sock.close()
