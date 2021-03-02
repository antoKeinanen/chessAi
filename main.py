import re
import chess
import chess.engine
import tables
import chess.polyglot
import chess.pgn
import datetime

board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("stockfish_13_win_x64_bmi2.exe")
move_history = []


def print_board():
    disp_board = str(board).split("\n")
    i = 8
    print()
    print(board.fullmove_number)
    print("   A B C D E F G H")
    print("=====================")
    for line in disp_board:
        print(f"{i}| {line} |{i}")
        i -= 1
    print("=====================")
    print("   A B C D E F G H")


def game_loop():
    moved = False
    while not moved:
        print_board()
        move_pat = re.compile("^[a-hA-H][1-8]")
        move = input("move: ").lower()
        move = move.split(" ")
        if move[0] == "pop":
            board.pop()
            board.pop()
            moved = True
        elif move_pat.match(move[0]) and move_pat.match(move[1]):
            if len(move) > 1:
                if board.is_legal(
                        chess.Move(from_square=chess.parse_square(move[0]), to_square=chess.parse_square(move[1]))):
                    board.push(
                        chess.Move(from_square=chess.parse_square(move[0]), to_square=chess.parse_square(move[1])))
                    moved = True
                else:
                    print("illegal move!")
            else:
                print("incorrect usage! usage: [from] [to]")
        else:
            print("incorrect usage! usage: [from] [to]")


def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    pawnsq = sum([tables.pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-tables.pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([tables.knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum(
        [-tables.knightstable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([tables.bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum(
        [-tables.bishopstable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([tables.rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-tables.rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([tables.queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum(
        [-tables.queenstable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([tables.kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-tables.kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval


def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore


def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha


def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader("bookfish.bin").weighted_choice(board).move()
        move_history.append(move)
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth-1)
            if boardValue > bestValue:
                bestValue = boardValue;
                bestMove = move
            if( boardValue > alpha ):
                alpha = boardValue
            board.pop()
        move_history.append(bestMove)
        return bestMove


if __name__ == '__main__':
    for i in range(40):
        game = chess.pgn.Game()
        game.headers["Event"] = "Test"
        game.headers["Site"] = "Kirjomäki"
        game.headers["Date"] = str(datetime.datetime.now().date())
        game.headers["Round"] = i
        game.headers["White"] = "pyChessAi"
        game.headers["Black"] = "Stockfish13"
        while not board.is_game_over(claim_draw=True):
            if board.turn:
                board.push(selectmove(2))
                print_board()
            else:
                result = engine.play(board, chess.engine.Limit(time=0.5))
                # print(f"{chess.square_name(result.move.from_square)} {chess.square_name(result.move.to_square)}")
                move_history.append(result.move)
                board.push(result.move)
                print_board()
        game.add_line(move_history)
        game.headers["Result"] = str(board.result())
        print(game, file=open(f"games/{i}.pgn", "w"), end="\n\n")
        board.reset()
        move_history = []



