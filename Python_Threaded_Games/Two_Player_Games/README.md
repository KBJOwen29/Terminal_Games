# Compiled Threaded Network Games

This version combines all four original games into **three Python files**:

- `server.py` — accepts two players, randomly selects the game chooser, and runs the selected game.
- `client.py` — one client program used by both players.
- `games.py` — contains all four game implementations.

## Included games

1. Tic-Tac-Toe
2. Connect Four
3. Blackjack
4. Hangman

## How the game selection works

1. Run `server.py` on the host computer.
2. Run `client.py` on both player computers.
3. When both players are connected, the server randomly chooses Player 1 or Player 2.
4. The randomly selected player receives the game menu.
5. The other player waits.
6. The selected game is loaded from `games.py`.
7. Both players play through the same `client.py`.

## Running it

### On the host computer

Open a terminal in this folder and run:

```bash
python server.py
```

Find the host computer's local/LAN IPv4 address, for example:

```text
192.168.1.10
```

### On both player computers

Run:

```bash
python client.py
```

When asked for the server IP, enter the host computer's LAN IP:

```text
192.168.1.10
```

## Important

All three files must be in the **same folder**:

```text
compiled_network_games/
├── server.py
├── client.py
├── games.py
└── README.md
```

Only the server needs to be run as `server.py`. Both players run the same `client.py`.

If Windows Firewall asks for permission, allow Python through the private network.

## Port

The combined server uses:

```text
5000
```

Unlike the original project, you no longer need separate ports for each game.

## Notes

- Exactly two players are supported.
- The game chooser is random for every server session.
- The game logic is centralized in `games.py`.
- Networking is centralized in `server.py` and `client.py`.
- No separate game-specific client/server files are required.
