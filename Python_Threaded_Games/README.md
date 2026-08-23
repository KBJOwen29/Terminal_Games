# Python Threaded Network Games

Included games:
- tic_tac_toe
- connect_four
- blackjack
- hangman

Each game has a `server.py` and `client.py`.

## Basic setup

1. Put the project on the host computer.
2. Run the desired `server.py`.
3. Find the host computer's LAN IP address.
4. Run `client.py` on each player's computer.
5. Enter the host IP when asked.

All games use TCP sockets and Python threads.

## Important

For computers on the same Wi-Fi/LAN, use the host's local IPv4 address, such as:
`192.168.1.10`

If Windows Firewall asks for permission, allow Python on the private network.

The ports are:
- Tic-Tac-Toe: 5000
- Connect Four: 5001
- Blackjack: 5002
- Hangman: 5003
