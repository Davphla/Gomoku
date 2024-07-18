# pbrain-gomoku-ai

This is a Gomoku AI written in Python. It uses the minimax algorithm with alpha-beta pruning and iterative deepening to find the best move. It also uses a transposition table to avoid repeating work.

## Prerequisites and compilation

The Piskvork manager is a Win32 application and currently supports only Win32 compatible .exe files (furthermore whose name starts with pbrain- prefix). There are several ways how to create .exe from Python files.


1. Install Windows (or [Wine](https://www.winehq.org/) for Linux)
2. Install [Python3](http://www.python.org)
3. Install [PyInstaller](https://www.pyinstaller.org/) and 
Install [Piskvork](https://sourceforge.net/projects/piskvork/) or
[PentaZen](https://github.com/sun-yuliang/PentaZen) or `make install`

## Usage

1. `make build-win` to compile the AI
2. Run the Piskvork manager and select `pbrain-gomoku-ai.exe` as the AI
3. Play against the AI
4. Enjoy!


- Run `make run` to run the AI and launch Piskvork for Linux with Wine
- Run `make run-win` to run the AI and launch Piskvork for Windows
- Run `make fclean` to remove the compiled AI
- Run `make test` to run the AI against itself
- Run `make uninstall` to uninstall Piskvork manager


## Architecture

- `main.py` - contains the main function
- `Client.py` - handles the main loop and connections with the server 
- `Agent.py` - contains the agent observations and actions logics
- `Communication.py` - handles the communication with the server
- `Protocol.py` - contains the protocol response logic
- `Policies/*Policy.py` - contains the policy logic
- `Policies/*Actions.py` - contains the policies actions logic

## Environment variables

- `DEBUG` - Add debug logs to stderr 
- `GMK_POLICY` - Gomoku policies (default: `RandomPolicy`)

