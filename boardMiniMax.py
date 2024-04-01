import board
import copy
import constants as const

class BoardMiniMax (board.Board):
    def __init__(self, player, x = 0, y = 0, matrix = [], parent=None, successors = []):
        super().__init__(player, x, y, matrix, parent, successors)
        
    def genSuccessor(self, x, y):
        if self.successors[x * const.COLS + y] is not None:
            return self.successors[x * const.COLS + y]
        
        newBoard = BoardMiniMax(self.nextPlayer(), x, y, self.matrix, self, successors=[])
        newBoard.matrix[x][y] = self.player
        newBoard.nrFullCells = self.nrFullCells + 1
        
        self.successors[x* const.COLS + y] = newBoard
        
        return newBoard
    
    # def genNextSuccessor(self, x = 0, y = 0):
    #     for i in range(x, const.ROWS):
    #         for j in range(const.COLS):
    #             if i == x and j == y:
    #                 continue
    #             elif self.canAddMove(i, j) and self.hasNeighbor(i, j):
    #                 return self.genSuccessor(i, j)
    #     return None
        
    
    def genSuccessors(self):        
        if len([1 for i in self.successors if i is not None]) != 0:
            return self.successors
        
        
        if self.isFull():
            return [None for _ in range(const.ROWS * const.COLS)]
        
        if self.winner() != None:
            return [None for _ in range(const.ROWS * const.COLS)]
        
        for i in range(const.ROWS):
            for j in range(const.COLS):
                if self.canAddMove(i, j) and self.hasNeighbor(i, j):
                    
                    newBoard = BoardMiniMax(self.nextPlayer(), i, j, self.matrix, self, successors=[])
                    newBoard.matrix[i][j] = self.player
                    newBoard.nrFullCells = self.nrFullCells + 1
                    
                    self.successors[i* const.COLS + j] = newBoard
        return self.successors
    
    def AIMakeMove(self):
        _, bestMove = self.minimax(4, True)
        newBoard = self.successors[bestMove[0] * const.COLS + bestMove[1]]
        return newBoard

    def minimax(self, depth, maximizingPlayer, alpha = float('-inf'), beta = float('inf')):
        successors = self.genSuccessors()
        # child = self.genNextSuccessor()
        if depth == 0 or len([1 for i in successors if i is not None]) == 0:
            if maximizingPlayer:
                return self.score(), None
            else:
                return -self.score(), None
        
        if maximizingPlayer:
            value = float('-inf')
            
            for child in successors:                
                if child is None:
                    continue
                
                eval, _ = child.minimax(depth - 1, False, alpha, beta)
                
                if eval > value:
                    value = eval
                    bestMove = (child.x, child.y)
                alpha = max(alpha, value)
                
                if beta <= alpha:
                    break
                
        else:
            value = float('inf')
            # child = self.genNextSuccessor()
            for child in successors:
                if child is None:
                    continue
                
                eval, _ = child.minimax(depth - 1, True, alpha, beta)
                if eval < value:
                    value = eval
                    bestMove = (child.x, child.y)
                    
                beta = min(beta, value)
                if beta <= alpha:
                    break
                
        return value, bestMove

