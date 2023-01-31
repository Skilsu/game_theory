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

    def setUpTree(self, p, symbol, i, short=True):
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
                j = self.has_symmetry(b)

                if not short:
                    s = self.gametree.create_node(symbol, parent=p, identifier=i, data=b)
                    s.data.symmetry_id = j
                if j < 0:
                    if short:
                        s = self.gametree.create_node(symbol, parent=p, identifier=i, data=b)
                    i = self.setUpTree(s, symbol, i, short)

            return i

    def getValue(self, node, symbol='X'):
        if node.data.isWinningBoard:
            return node.data.isWinningBoardValue
        else:
            res = []
            for x in node.successors(self.gametree.identifier):
                res.append(self.getValue(self.gametree.get_node(x), symbol))
            if len(res) == 0:
                return node.data.isWinningBoardValue
            else:
                if node.data.symbol == symbol:
                    return max(res)
                else:
                    return min(res)

    def getValue_alpha_beta(self, node, alpha=-math.inf, beta=math.inf, symbol='X'):
        if node.data.isWinningBoard:
            return node.data.isWinningBoardValue
        else:
            if node.data.symbol == symbol:
                value = float('-inf')
                for x in node.successors(self.gametree.identifier):
                    value = max(value, self.getValue_alpha_beta(self.gametree.get_node(x), alpha, beta, symbol))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value
            else:
                value = float('inf')
                for x in node.successors(self.gametree.identifier):
                    value = min(value, self.getValue_alpha_beta(self.gametree.get_node(x), alpha, beta, symbol='O'))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                if len(node.successors(self.gametree.identifier)) == 0:
                    return node.data.isWinningBoardValue
                else:
                    return value

    def has_symmetry(self, data):
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
        return self.getValue(self.gametree.get_node(self.has_symmetry(board)))

    def minimax_neu(self, board):
        return self.getValue(self.gametree.get_node(self.has_symmetry(board)), symbol='O')

    def baMax_neu(self, board):
        return self.getValue_alpha_beta(self.gametree.get_node(self.has_symmetry(board)))

    def baMin_neu(self, board):
        return self.getValue_alpha_beta(self.gametree.get_node(self.has_symmetry(board)), symbol='O')


def main():
    ttt = TicTacToeGame()
    root = ttt.gametree.get_node(0)
    ttt.setUpTree(root, 'X', 0, short=True)
    print(ttt.getValue(root))
    print(len(ttt.gametree.all_nodes()))


if __name__ == "__main__":
    main()
