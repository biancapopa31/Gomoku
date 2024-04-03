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
            return "remiza"
        
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
        if winner == self.player:
            return 100
        elif winner == self.nextPlayer():
            return -100
        elif winner == "remiza":
            return 0
        
        return scor
        
        # for i in range(const.ROWS):
        #     for dir in range(4):
        #         x, y = directions[dir]
        #         v = self.getVector(i, 0, x, y)
        #         self.evalVector(v)
                
        #     self.evalVector(i, 0, 0, 1)
            
            
            
    def score_lung(self):
        
        winner = self.winner()
        if winner == self.player:
            return 100
        elif winner == self.nextPlayer():
            return -100
        elif winner == "remiza":
            return 0

        score = 0
        opponent = self.nextPlayer()  # Identify opponent

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for row in range(const.ROWS):
            for col in range(const.COLS):
                empty_cell = self.matrix[row][col] is None

                # Score for player's potential lines, considering blocking opportunities
                if empty_cell or self.matrix[row][col] == self.player:
                    consecutive_count = 1
                    potential_block = False  # Flag to identify potential blocking opportunity
                    for direction in directions:
                        r, c = row, col
                        while 0 <= r + direction[0] < const.ROWS and 0 <= c + direction[1] < const.COLS and (self.matrix[r + direction[0]][c + direction[1]] == self.player or empty_cell):
                            consecutive_count += 1
                            if self.matrix[r + direction[0]][c + direction[1]] == empty_cell and (0 in (r + direction[0], c + direction[1]) or const.ROWS - 1 in (r + direction[0], c + direction[1])):
                                potential_block = True  # Potential to block opponent's line
                            r += direction[0]
                            c += direction[1]

                        # Score with bonus for blocking opportunities near the edge
                        if consecutive_count >= 4 and (0 in (row, col, r, c) or const.ROWS - 1 in (row, col, r, c)):
                            score += consecutive_count ** (2 if potential_block else 1.5)

                # Penalty for opponent's potential lines (but not immediate threats)
                if empty_cell or self.matrix[row][col] == opponent:
                    consecutive_count = 1
                    for direction in directions:
                        r, c = row, col
                        while 0 <= r + direction[0] < const.ROWS and 0 <= c + direction[1] < const.COLS and (self.matrix[r + direction[0]][c + direction[1]] == opponent or empty_cell):
                            consecutive_count += 1
                            r += direction[0]
                            c += direction[1]

                        if consecutive_count >= 4:  # Penalize potential opponent lines (not immediate threats)
                            score -= consecutive_count ** 1.2

        # Bonus for forks (threatening two lines) and potential double forks
        for row in range(const.ROWS):
            for col in range(const.COLS):
                if self.matrix[row][col] == self.player:
                    fork_count = 0
                    double_fork_count = 0  # Track potential for double forks
                    for direction in directions:
                        if 0 <= row + direction[0] < const.ROWS and 0 <= col + direction[1] < const.COLS and self.matrix[row + direction[0]][col + direction[1]] == '.':
                            fork_count += 1
                            # Check for empty cell in opposite direction for potential double fork
                            if 0 <= row - direction[0] < const.ROWS and 0 <= col - direction[1] < const.COLS and self.matrix[row - direction[0]][col - direction[1]] == '.':
                                double_fork_count += 1
                        if fork_count >= 2:
                            score += 3  # Bonus for each fork
                        if double_fork_count >= 2:
                            score += 5  # Higher bonus for potential double fork


        return score


            
    def getVector(self, x, y, dirX, dirY):
        v = []
        while x >= 0 and x < const.ROWS and y >= 0 and y < const.COLS:
            v.append(self.matrix[x][y])
            x = x + dirX
            y = y + dirY
        return v
