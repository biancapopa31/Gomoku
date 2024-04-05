import pygame
import copy
import constants as const

pygame.init()

directions = [(1, 0), (0, 1), (1, 1), (1, -1)]


class Board:
    def __init__(self, player, x = 0, y = 0, matrix = [], parent=None, successors = []):
        self.player = player # jucatorul care trbuie sa faca mutarea
        
        if matrix == []:
            self.matrix = [[None for _ in range(const.COLS)] for _ in range(const.ROWS)]
        else:
            self.matrix = copy.deepcopy(matrix)
            
        self.nrFullCells = 0
        self.parent = parent
        
        # coordonatele ultimei mutari
        self.x = x
        self.y = y
        
        if successors == []:
            self.successors = [None for _ in range(const.ROWS * const.COLS)]
        else:
            self.successors = copy.deepcopy(successors)
         
    
    def __str__(self):

        matrix_to_stringify = copy.copy(self.matrix)

        for row in range(const.ROWS):
            for col in range(const.COLS):
                if matrix_to_stringify[row][col] is None:
                    matrix_to_stringify[row][col] = '-'  

        string_representation = f"Player: {self.player}\n"
        for row in matrix_to_stringify:
            string_representation += '|' + '|'.join(str(cell) for cell in row) + '|\n'

        return string_representation     
       
    def __eq__(self, other):
        for i in range (const.ROWS):
            for j in range (const.COLS):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True
    
    def __hash__(self):
        matrix_str = str(self.matrix)

        matrix_hash = hash(matrix_str)

        return matrix_hash


    def getVal(self, x, y):
        return self.matrix[x][y]
    
    def getPlayer(self):
        return self.player
    
    def nextPlayer(self):
        if self.player == const.BLACK:
            return const.WHITE
        return const.BLACK
    
    def isFull(self):     
        if self.nrFullCells == const.ROWS * const.COLS:
            return True
        return False

    def canAddMove(self, x, y):
        if self.matrix[x][y] != None:
            return False
        return True
    
    def addMove(self, x, y): # returneaza un nou board cu mutarea adaugata
        if self.nrFullCells == 0:
            print("Prima mutare")
            newBoard = Board(self.nextPlayer(), x, y, self.matrix, self, successors=[])
            newBoard.matrix[x][y] = self.player
            newBoard.nrFullCells = self.nrFullCells + 1
            return newBoard
        self.genSuccessors()
        # print("In AddMove " + str(len([1 for i in self.successors if i is not None])))
        return self.successors[x * const.COLS + y]
        
            
    def hasNeighbor(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if x + i >= 0 and x + i < const.ROWS and y + j >= 0 and y + j < const.COLS:
                    if self.matrix[x + i][y + j] != None:
                        return True
        return False
    
    def genSuccessors(self):
        if len([1 for i in self.successors if i is not None]) != 0:
            return self.successors
        
        if self.isFull():
            return [None for _ in range(const.ROWS * const.COLS)]
        
        if self.winner() != None:
            return [None for _ in range(const.ROWS * const.COLS)]
        
        for i in range(const.ROWS):
            for j in range(const.COLS):
                if self.canAddMove(i, j):
                    
                    newBoard = Board(self.nextPlayer(), i, j, self.matrix, self)
                    newBoard.matrix[i][j] = self.player
                    newBoard.nrFullCells = self.nrFullCells + 1
                    
                    self.successors[i* const.COLS + j] = newBoard
        return self.successors
    
    
    def winner(self): # returneaza jucatorul castigator sau None daca nu exista castigator
        if self.isFull():
            return const.DRAW
        
        for i in range (const.ROWS):
            for j in range(const.COLS):
                if self.matrix[i][j] == None:
                    continue
                if i + 4 < const.ROWS:
                    if self.matrix[i][j] == self.matrix[i+1][j] == self.matrix[i+2][j] == self.matrix[i+3][j] == self.matrix[i+4][j]:
                        return self.matrix[i][j]
                if j + 4 < const.COLS:
                    if self.matrix[i][j] == self.matrix[i][j+1] == self.matrix[i][j+2] == self.matrix[i][j+3] == self.matrix[i][j+4]:
                        return self.matrix[i][j]
                if i + 4 < const.ROWS and j + 4 < const.COLS:
                    if self.matrix[i][j] == self.matrix[i+1][j+1] == self.matrix[i+2][j+2] == self.matrix[i+3][j+3] == self.matrix[i+4][j+4]:
                        return self.matrix[i][j]
                if i + 4 < const.ROWS and j - 4 >= 0:
                    if self.matrix[i][j] == self.matrix[i+1][j-1] == self.matrix[i+2][j-2] == self.matrix[i+3][j-3] == self.matrix[i+4][j-4]:
                        return self.matrix[i][j]
        return None
    
    def score(self): # returneaza valoarea board-ului
        scor = 0
        winner = self.winner()
        if winner == const.BLACK:
            return -100000
        elif winner == const.WHITE:
            return +100000
        elif winner == const.DRAW:
            return 0
                
        for i in range(const.ROWS):
            x, y = directions[0] # directia verticala (1, 0)
            v = self.getVector(0, i, x, y)
            scor -= self.evalVector(v, const.BLACK)
            scor += self.evalVector(v, const.WHITE)
            # print(v)
            
            x,y = directions[1] # directia orizontala (0, 1)
            v = self.getVector(i, 0, x, y)
            scor -= self.evalVector(v, const.BLACK)
            scor += self.evalVector(v, const.WHITE)
            # print(v)
            
            x,y = directions[2] # directia diagonala principala (1, 1)
            v = self.getVector(i, 0, x, y)
            scor -= self.evalVector(v, const.BLACK)
            scor += self.evalVector(v, const.WHITE)
            # print(v)
            if(i != 0):
                v = self.getVector(0, i, x, y)
                scor -= self.evalVector(v, const.BLACK)
                scor += self.evalVector(v, const.WHITE)
                # print(v)
            
            x,y = directions[3] # directia diagonala secundara (1, -1)
            v = self.getVector(0, i, x, y)
            scor -= self.evalVector(v, const.BLACK)
            scor += self.evalVector(v, const.WHITE)
            # print(v)
            if(i != 0):
                v = self.getVector(i, const.ROWS-1, x, y)
                scor -= self.evalVector(v, const.BLACK)
                scor += self.evalVector(v, const.WHITE)
                # print(v)
                
                
        return scor
            
    def getVector(self, x, y, dirX, dirY):
        v = []
        while x >= 0 and x < const.ROWS and y >= 0 and y < const.COLS:
            v.append(self.matrix[x][y])
            x = x + dirX
            y = y + dirY
        return v
    
    def evalVector(self, v, player):
        if len(v) < 5:
            return 0
        eval = 0
        for i in range(len(v) - 4):
            eval += self.evalSeq(v[i:i+5], player)
                    
        return eval
    def evalSeq(self, seq, player):
        if seq.count(player) == 4 and seq.count(None) == 1:
            return 1000
        if seq.count(player) == 3 and seq.count(None) == 2:
            return 100
        if seq.count(player) == 2 and seq.count(None) == 3:
            return 10
        if seq.count(player) == 1 and seq.count(None) == 4:
            return 1
        return 0
    


