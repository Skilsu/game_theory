import math

from treelib import Node, Tree
import copy
import datetime


class TicTacToeBoard:

    def __init__(self, *args):
        if len(args) == 0:
            self.board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
        else:
            self.board = args[0]
        self.isWinningBoard = False
        self.isWinningBoardValue = 0
        self.symbol = ' '
        self.symmetry_id = -1
        self.minimax = 0
        self.alpha = 0
        self.beta = 0

    def printBoard(self):
        for i in self.board:
            print(i)

    def expand(self, symbol):
        self.symbol = symbol
        nextmoves = []
        if not self.isWinning():
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if self.board[i][j] == "_":
                        newboard = copy.deepcopy(self.board)
                        newboard[i][j] = symbol
                        nextmoves.append(TicTacToeBoard(newboard))
        return nextmoves

    def isWinning(self):
        b = self.board
        res = False
        for i in range(len(b)):
            if b[i][0] == b[i][1] and b[i][0] == b[i][2] and b[i][0] != '_':
                if b[i][0] == 'X':
                    self.isWinningBoardValue = 1
                else:
                    self.isWinningBoardValue = -1
                res = True
            if b[0][i] == b[1][i] and b[0][i] == b[2][i] and b[0][i] != '_':
                if b[0][i] == 'X':
                    self.isWinningBoardValue = 1
                else:
                    self.isWinningBoardValue = -1
                res = True
        if b[0][0] == b[1][1] and b[0][0] == b[2][2] and b[0][0] != '_':
            if b[0][0] == 'X':
                self.isWinningBoardValue = 1
            else:
                self.isWinningBoardValue = -1
            res = True
        if b[0][2] == b[1][1] and b[0][2] == b[2][0] and b[0][2] != '_':
            if b[0][2] == 'X':
                self.isWinningBoardValue = 1
            else:
                self.isWinningBoardValue = -1
            res = True
        if res:
            self.isWinningBoard = True
        return res


class TicTacToeGame:

    def __init__(self, *args):
        self.gametree = Tree()
        if len(args) == 0:
            self.gametree.create_node("root", identifier=0, data=TicTacToeBoard())
        else:
            self.gametree.create_node("root", identifier=0, data=TicTacToeBoard(args[0]))

    def printTree(self):
        self.gametree.get_node(0).data.printBoard()

    def setUpTree(self, p, symbol, i):
        x = p.data.expand(symbol)
        if len(x) == 0:
            # p.data.minimax = p.data.isWinningBoardValue
            return i
        else:
            if symbol == 'X':
                symbol = 'O'
            else:
                symbol = 'X'
            for b in x:
                i = i + 1
                j = self.has_symmetry_ultra_short(b)

                if j < 0:
                    s = self.gametree.create_node(symbol, parent=p, identifier=i, data=b)
                    i = self.setUpTree(s, symbol, i)
                else:
                    pass
                    # s.data.symmetry_id = j
                # TODO minimax
                # TODO alphabeta
            return i

    def getValue(self, node):
        if node.data.isWinningBoard:
            return node.data.isWinningBoardValue
        else:
            res = []
            for x in node.successors(self.gametree.identifier):
                res.append(self.getValue(self.gametree.get_node(x)))
            if len(res) == 0:
                return node.data.isWinningBoardValue
            else:
                if node.data.symbol == 'X':
                    return max(res)
                else:
                    return min(res)

    def exp(self):
        for idx in self[0].successors(self.gametree.identifier):
            node = self.gametree.get_node(idx)
            print(id, node)

    def has_symmetry(self, data):
        boards = [data.board]
        # horizontal gespiegelt
        boards.append([boards[0][2], boards[0][1], boards[0][0]])
        # vertikal gespiegelt
        brd = []
        for i in boards:
            brd.append([[i[0][2], i[0][1], i[0][0]],
                        [i[1][2], i[1][1], i[1][0]],
                        [i[2][2], i[2][1], i[2][0]]])
        for i in brd:
            boards.append(i)
        # diagonal achse von ol nach ur
        brd = []
        for i in boards:
            brd.append([[i[0][0], i[1][0], i[2][0]],
                        [i[0][1], i[1][1], i[2][1]],
                        [i[0][2], i[1][2], i[2][2]]])
        for i in brd:
            boards.append(i)
        # diagonal achse von or nach ul
        brd = []
        for i in boards:
            brd.append([[i[2][2], i[1][2], i[0][2]],
                        [i[2][1], i[1][1], i[0][1]],
                        [i[2][0], i[1][0], i[0][0]]])
        for i in brd:
            boards.append(i)
        # 180° Drehung
        brd = []
        for i in boards:
            brd.append([[i[2][2], i[2][1], i[2][0]],
                        [i[1][2], i[1][1], i[1][0]],
                        [i[0][2], i[0][1], i[0][0]]])
        for i in brd:
            boards.append(i)
        # 90° Drehung
        brd = []
        for i in boards:
            brd.append([[i[2][0], i[1][0], i[0][0]],
                        [i[2][1], i[1][1], i[0][1]],
                        [i[2][2], i[1][2], i[0][2]]])
        for i in brd:
            boards.append(i)

        for node_board in self.gametree.all_nodes()[:]:
            for sym_board in boards:
                if node_board.data.board == sym_board:
                    return node_board.identifier
        return -1

    def has_symmetry_optimized(self, data):
        boards = [data.board]
        # horizontal gespiegelt
        boards.append([boards[0][2], boards[0][1], boards[0][0]])
        # vertikal gespiegelt
        brd = []
        for i in boards:
            brd.append([[i[0][2], i[0][1], i[0][0]],
                        [i[1][2], i[1][1], i[1][0]],
                        [i[2][2], i[2][1], i[2][0]]])
        for i in brd:
            boards.append(i)
        # diagonal achse von ol nach ur
        brd = []
        for i in boards:
            brd.append([[i[0][0], i[1][0], i[2][0]],
                        [i[0][1], i[1][1], i[2][1]],
                        [i[0][2], i[1][2], i[2][2]]])
        for i in brd:
            boards.append(i)
        # diagonal achse von or nach ul
        brd = []
        for i in boards:
            brd.append([[i[2][2], i[1][2], i[0][2]],
                        [i[2][1], i[1][1], i[0][1]],
                        [i[2][0], i[1][0], i[0][0]]])
        for i in brd:
            boards.append(i)
        # 180° Drehung
        brd = []
        for i in boards:
            brd.append([[i[2][2], i[2][1], i[2][0]],
                        [i[1][2], i[1][1], i[1][0]],
                        [i[0][2], i[0][1], i[0][0]]])
        for i in brd:
            boards.append(i)
        # 90° Drehung
        brd = []
        for i in boards:
            brd.append([[i[2][0], i[1][0], i[0][0]],
                        [i[2][1], i[1][1], i[0][1]],
                        [i[2][2], i[1][2], i[0][2]]])
        for i in brd:
            boards.append(i)

        new_boards = []
        for i in boards:
            if i not in new_boards:
                new_boards.append(i)
        boards = new_boards

        for node_board in self.gametree.all_nodes()[:]:
            for sym_board in boards:
                if node_board.data.board == sym_board:
                    return node_board.identifier
        return -1

    def has_symmetry_short(self, data):
        boards = [data.board]
        # horizontal gespiegelt
        boards.append([boards[0][2], boards[0][1], boards[0][0]])
        # 90° Drehung
        brd = []
        for i in boards:
            brd.append([[i[2][0], i[1][0], i[0][0]],
                        [i[2][1], i[1][1], i[0][1]],
                        [i[2][2], i[1][2], i[0][2]]])
        for i in brd:
            boards.append(i)
        # diagonal achse von or nach ul
        brd = []
        for i in boards:
            brd.append([[i[2][2], i[1][2], i[0][2]],
                        [i[2][1], i[1][1], i[0][1]],
                        [i[2][0], i[1][0], i[0][0]]])
        for i in brd:
            boards.append(i)

        for node_board in self.gametree.all_nodes()[:]:
            for sym_board in boards:
                if node_board.data.board == sym_board:
                    return node_board.identifier
        return -1

    def has_symmetry_ultra_short(self, data):
        boards = [data.board]
        # horizontal gespiegelt
        boards.append([boards[0][2], boards[0][1], boards[0][0]])
        # 90° Drehung
        b_len = len(boards)
        for i in range(b_len):
            boards.append([[boards[i][2][0], boards[i][1][0], boards[i][0][0]],
                           [boards[i][2][1], boards[i][1][1], boards[i][0][1]],
                           [boards[i][2][2], boards[i][1][2], boards[i][0][2]]])
        # diagonal achse von or nach ul
        b_len = len(boards)
        for i in range(b_len):
            boards.append([[boards[i][2][2], boards[i][1][2], boards[i][0][2]],
                           [boards[i][2][1], boards[i][1][1], boards[i][0][1]],
                           [boards[i][2][0], boards[i][1][0], boards[i][0][0]]])

        for node_board in self.gametree.all_nodes()[:]:
            for sym_board in boards:
                if node_board.data.board == sym_board:
                    return node_board.identifier
        return -1

    def has_symmetry_ultra_short_hardcoded(self, data):
        boards = [data.board]
        # horizontal gespiegelt
        boards.append([boards[0][2], boards[0][1], boards[0][0]])
        boards.append([[boards[0][2][0], boards[0][1][0], boards[0][0][0]],
                       [boards[0][2][1], boards[0][1][1], boards[0][0][1]],
                       [boards[0][2][2], boards[0][1][2], boards[0][0][2]]])
        boards.append([[boards[1][2][0], boards[1][1][0], boards[1][0][0]],
                       [boards[1][2][1], boards[1][1][1], boards[1][0][1]],
                       [boards[1][2][2], boards[1][1][2], boards[1][0][2]]])
        # diagonal achse von or nach ul
        boards.append([[boards[0][2][2], boards[0][1][2], boards[0][0][2]],
                       [boards[0][2][1], boards[0][1][1], boards[0][0][1]],
                       [boards[0][2][0], boards[0][1][0], boards[0][0][0]]])
        boards.append([[boards[1][2][2], boards[1][1][2], boards[1][0][2]],
                       [boards[1][2][1], boards[1][1][1], boards[1][0][1]],
                       [boards[1][2][0], boards[1][1][0], boards[1][0][0]]])
        boards.append([[boards[2][2][2], boards[2][1][2], boards[2][0][2]],
                       [boards[2][2][1], boards[2][1][1], boards[2][0][1]],
                       [boards[2][2][0], boards[2][1][0], boards[2][0][0]]])
        boards.append([[boards[3][2][2], boards[3][1][2], boards[3][0][2]],
                       [boards[3][2][1], boards[3][1][1], boards[3][0][1]],
                       [boards[3][2][0], boards[3][1][0], boards[3][0][0]]])

        for node_board in self.gametree.all_nodes()[:]:
            for sym_board in boards:
                if node_board.data.board == sym_board:
                    return node_board.identifier
        return -1

    def baMin(self, board, alpha=-math.inf, beta=math.inf):
        # print("bamin",alpha,beta)
        if board.isWinning():
            return board.isWinningBoardValue
        nextmoves = board.expand("O")
        if len(nextmoves) == 0:
            return board.isWinningBoardValue
        minwert = beta
        for x in nextmoves:
            w = self.baMax(x, alpha, minwert)
            if w < minwert:
                minwert = w
            if minwert <= alpha:
                return minwert
        return minwert

    def baMax(self, board, alpha=-math.inf, beta=math.inf):
        # print("bamax",alpha, beta)
        if board.isWinning():
            return board.isWinningBoardValue
        nextmoves = board.expand("X")
        if len(nextmoves) == 0:
            return board.isWinningBoardValue
        maxwert = alpha
        for x in nextmoves:
            w = self.baMin(x, maxwert, beta)
            if w > maxwert:
                maxwert = w
            if maxwert >= beta:
                return maxwert
        return maxwert

    def minimax(self, board):
        if board.isWinning():
            return board.isWinningBoardValue
        nextmoves = board.expand("O")
        if len(nextmoves) == 0:
            return board.isWinningBoardValue
        res = []
        for x in nextmoves:
            res.append(self.maximin(x))
        return min(res)

    def maximin(self, board):
        if board.isWinning():
            return board.isWinningBoardValue
        nextmoves = board.expand("X")
        if len(nextmoves) == 0:
            return board.isWinningBoardValue
        res = []
        for x in nextmoves:
            res.append(self.minimax(x))
        return max(res)

    def maximin_neu(self, board):
        return self.getValue(self.gametree.get_node(self.has_symmetry_ultra_short(board)))


def exp():
    ttt = TicTacToeGame()
    root = ttt.gametree.get_node(0)
    print("ROOT", root.successors(ttt.gametree.identifier))
    ttt.setUpTree(root, 'X', 0)
    print(len(ttt.gametree.leaves()))
    print(ttt.getValue(root))

    for id in root.successors(ttt.gametree.identifier):
        node = ttt.gametree.get_node(id)
        print(id, node)

    maxnf = True
    minnf = True
    drawnf = True
    for n in ttt.gametree.leaves():
        val = ttt.getValue(n)
        if val == 1 and maxnf:
            print("max")
            print(n.identifier)
            n.data.printBoard()
            maxnf = False
        if val == -1 and minnf:
            print("min")
            print(n.identifier)
            n.data.printBoard()
            minnf = False
        if val == 0 and drawnf:
            print("Draw")
            print(n.identifier)
            n.data.printBoard()
            drawnf = False
        if not minnf and not maxnf and not drawnf:
            break


def main3():
    ttt = TicTacToeGame()
    root = ttt.gametree.get_node(0)
    ttt.setUpTree(root, 'X', 0)
    print(ttt.getValue(root))
    print(len(ttt.gametree.all_nodes()))
    # print(TicTacToeGame().maximin(TicTacToeBoard([['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']])))
    '''for i in range(100):
        print(ttt.gametree.get_node(i).data.symmetry_id)'''


def main4():
    ergebnis = 0
    erg_min = 100000000000
    erg_max = 0
    for i in range(100):
        t1 = datetime.datetime.now()
        main3()
        t2 = datetime.datetime.now()
        t3 = t2 - t1
        zwischen_ergebnis = t3.microseconds
        zwischen_ergebnis += t3.seconds * 1000000
        ergebnis += zwischen_ergebnis
        if erg_min > zwischen_ergebnis:
            erg_min = zwischen_ergebnis
        if erg_max < zwischen_ergebnis:
            erg_max = zwischen_ergebnis
        print(f"{i=}, {t3=}, {ergebnis=}, {zwischen_ergebnis=}, {erg_max=}, {erg_min=}")

    print(ergebnis / 100)
    print(float(ergebnis / 100000000))
    print(f"{erg_min=}, {erg_max=}")


def main5():
    board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]


def main():
    board = TicTacToeBoard([['X', 'O', 'X'], ['X', 'O', '_'], ['O', '_', '_']])
    t1 = datetime.datetime.now()
    ttt = TicTacToeGame(board.board)
    root = ttt.gametree.get_node(0)
    ttt.setUpTree(root, 'X', 0)
    t2 = datetime.datetime.now()

    t3 = t2 - t1
    optimized_erg = t3.microseconds
    optimized_erg += t3.seconds * 1000000

    t1 = datetime.datetime.now()
    x = TicTacToeGame().maximin(board)
    t2 = datetime.datetime.now()

    t3 = t2 - t1
    minimax_erg = t3.microseconds
    minimax_erg += t3.seconds * 1000000

    t1 = datetime.datetime.now()
    y = TicTacToeGame().baMax(board)
    t2 = datetime.datetime.now()

    t3 = t2 - t1
    alphabeta_erg = t3.microseconds
    alphabeta_erg += t3.seconds * 1000000
    print(len(ttt.gametree.all_nodes()))

    t1 = datetime.datetime.now()
    z = ttt.getValue(ttt.gametree.get_node(0))
    t2 = datetime.datetime.now()

    t3 = t2 - t1
    method_erg = t3.microseconds
    method_erg += t3.seconds * 1000000
    print(len(ttt.gametree.all_nodes()))
    print(x, y, z)
    print(f"{optimized_erg=}, {minimax_erg=}, {alphabeta_erg=}, {method_erg=}")
    print(ttt.maximin_neu(board))


if __name__ == "__main__":
    main()
