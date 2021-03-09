# ChessAi
ChessAi is a simple chess computer made using python.

![](https://img.shields.io/github/stars/antoKeinanen/chessAi) 
![](https://img.shields.io/github/forks/antoKeinanen/chessAi)
![](https://img.shields.io/github/release/antoKeinanen/chessAi) 
![](https://img.shields.io/github/issues/antoKeinanen/chessAi)
[![Run on Repl.it](https://repl.it/badge/github/antoKeinanen/chessAi)](https://repl.it/github/antoKeinanen/chessAi)

## Installation
Enter the following commands to in commandline or shell.
``git clone https://github.com/antoKeinanen/chessAi.git``

``cd chessAi``

If you don't have PIP you can install it [HERE](https://pip.pypa.io/en/stable/installing/).

``pip install -r requirements.txt``

## Usage
### If you want to play against ai
run ai.py file using ``python3 ai.py`` in commandline or shell.

```shell
1
   A B C D E F G H
=====================
8| r n b q k b n r |8
7| p p p p p p p p |7
6| . . . . . . . . |6
5| . . . . . . . . |5
4| . . . . . . . . |4
3| . . . . . . . . |3
2| P P P P P P P P |2
1| R N B Q K B N R |1
=====================
   A B C D E F G H
move: 
```
Enter your move in {from square} {to square} format.
Capital letters are white pieces and lowercase are black pieces.

```shell
P = Pawn
R = Rook
N = Knight
B = Bishop 
Q = Queen
K = King
```

### If you want to watch my ai to play against stockfish the leading chess ai
run main.py file using ``python3 main.py`` in commandline or shell.

## Roadmap
I still plan to add some chess variations like atomic-chess, crazy house and, chess 960.

## Acknowledgment
Special thanks to GitHub user [niklasf](https://github.com/niklasf) for letting me use his python-chess library.

## Support/Ideas/Feedback
Leave me a message in discussions tab!

## License
[gpl-3.0](https://choosealicense.com/licenses/gpl-3.0/)
