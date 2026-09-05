# Terminal Games

A collection of classic games playable entirely in the terminal, built in Python. The repo has two flavors:

- **`Python/`** — single-player-friendly, single-file games you run and play locally.
- **`Python_Threaded_Games/`** — the same idea, but networked: a `server.py` and `client.py` per game, using TCP sockets and threads so you can play over LAN with a friend.

## Requirements

- Python 3.x (developed/tested on Python 3.12)
- No third-party libraries required — everything uses Python's standard library

## Games

### `Python/` — local games

| Game | Folder | Run |
|---|---|---|
| Black Jack | `Python/Black_Jack` | `python black_jack.py` |
| Chess | `Python/Chess` | `python chess.py` |
| Connect Four | `Python/Connect_Four` | `python connect_four.py` |
| Number Guess | `Python/Number_Guess` | `python number_guess.py` |
| Rock Paper Scissors | `Python/Rock_Paper_Scissors` | `python Rock_Paper_Scissors.py` |
| Tic Tac Toe | `Python/TicTacToe` | `python TicTacToe.py` |
| Wordle | `Python/Wordle` | `python wordle.py` |

Chess and Connect Four are two-player, pass-and-play on one keyboard. Black Jack is played against the computer. Number Guess, Rock Paper Scissors, and Wordle are single-player.

**Chess controls:** enter moves as `e2 e4` (from-square, space, to-square); type `quit` to exit.

### `Python_Threaded_Games/` — play over LAN

| Game | Folder | Port |
|---|---|---|
| Tic-Tac-Toe | `Python_Threaded_Games/Tic_Tac_Toe` | 5000 |
| Connect Four | `Python_Threaded_Games/Connect_Four` | 5001 |
| Blackjack | `Python_Threaded_Games/Blackjack` | 5002 |
| Hangman | `Python_Threaded_Games/Hangman` | 5003 |
| Two Player Games | `Python_Threaded_Games/Two_Player_Games` | — |

Each game folder has its own `server.py` and `client.py`.

**Basic setup:**
1. Put the project on the host computer.
2. Run the desired game's `server.py` on the host.
3. Find the host computer's LAN IPv4 address (e.g. `192.168.1.10`).
4. Run `client.py` on each player's computer.
5. When prompted, enter the host's IP address.

> If Windows Firewall prompts for permission, allow Python on the private network. All devices need to be on the same Wi-Fi/LAN.

## Getting Started

Clone the repo:

```bash
git clone https://github.com/KBJOwen29/Terminal_Games.git
cd Terminal_Games
```

Pick a game and run it, e.g.:

```bash
cd Python/TicTacToe
python TicTacToe.py
```

Or for a networked game:

```bash
cd Python_Threaded_Games/Blackjack
python server.py
# on each client machine:
python client.py
```

## Project Structure

```
Terminal_Games/
├── Python/                     # local, single-run games
│   ├── Black_Jack/
│   ├── Chess/
│   ├── Connect_Four/
│   ├── Number_Guess/
│   ├── Rock_Paper_Scissors/
│   ├── TicTacToe/
│   └── Wordle/
└── Python_Threaded_Games/       # networked games (server + client)
    ├── Blackjack/
    ├── Connect_Four/
    ├── Hangman/
    ├── Tic_Tac_Toe/
    └── Two_Player_Games/
```

## Contributing

Suggestions and pull requests for new terminal games are welcome — feel free to open an issue or PR.

## License

No license specified yet.
