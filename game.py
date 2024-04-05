import pygame
import time
import board
import boardMiniMax
import utils
import constants as const

# pygame setup

class Game:
    def __init__(self, alg, dif):
        self.screenSetup()
        
        if(alg == const.MINIMAX):
            self.board = boardMiniMax.BoardMiniMax(const.BLACK)
        # else:
            # self.board = board.Board(const.BLACK)

        self.running = True
        self.startTime = time.time()
        const.DEPTH = dif        
        self.run()

    # Setting up the screen's size, color, and top text.
    def screenSetup(self):
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption("Go-Moku")
        self.screen.fill(const.BACKGROUND_COLOR)

        self.font = pygame.font.SysFont(None, 30)


    def drawTurnText(self):
        # Render the text
        text = self.font.render("Black" if self.board.getPlayer() == const.BLACK else "White", True, const.LINE_COLOR)

        # Calculate text position
        text_rect = text.get_rect(center=(const.SCREEN_WIDTH // 2, const.COLS_OFFSET//3))
        self.screen.blit(text, text_rect)

    def drawTime(self):
        timePassed = time.time() - self.startTime
        seconds = int(timePassed % 60)
        minutes = int(timePassed // 60)

          # Render the text
        text = self.font.render(f"Time: {minutes}:{seconds}", True, const.LINE_COLOR)

        # Calculate text position
        text_rect = text.get_rect(center=(const.SCREEN_WIDTH // 2, const.COLS_OFFSET * 2 //3))
        self.screen.blit(text, text_rect)
        
        
    def drawCircle(self, coords, player):
        if player == const.BLACK:
            pygame.draw.circle(self.screen, const.BLACK_COLOR, coords, const.CIRCLE_RADIUS)
        else:
            pygame.draw.circle(self.screen, const.WHITE_COLOR, coords, const.CIRCLE_RADIUS)

    def drawBoard(self):

        #Draw column lines
        for i in range(const.COLS):
            pygame.draw.line(self.screen, const.LINE_COLOR, (const.ROWS_OFFSET + i * const.CELL_SIZE, const.COLS_OFFSET), (const.ROWS_OFFSET + i * const.CELL_SIZE, (const.COLS-1)* const.CELL_SIZE + const.COLS_OFFSET), 1)
        
        #Draw row lines
        for i in range(const.ROWS):
            pygame.draw.line(self.screen, const.LINE_COLOR, (const.ROWS_OFFSET, const.COLS_OFFSET + i* const.CELL_SIZE), (const.ROWS_OFFSET + (const.ROWS-1) * const.CELL_SIZE, const.COLS_OFFSET + i * const.CELL_SIZE), 1)
        
        for i in range(const.COLS):
            for j in range(const.ROWS):
                if self.board.getVal(i,j) != None:
                    self.drawCircle(utils.indexToCoords(i, j), self.board.getVal(i,j))
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # print("In for: " + str(type(self.board)))
                if self.board.getPlayer() == const.BLACK:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        board_x, board_y = utils.coordsToIndex(mouse_x, mouse_y)
                        
                        if board_x != None:
                            if self.board.canAddMove(board_x, board_y):
                                self.board = self.board.addMove(board_x, board_y)
                                
                                self.screen.fill(const.BACKGROUND_COLOR)
                                self.drawTurnText()
                                self.drawTime()
                                self.drawBoard()
                                pygame.display.flip()
                                
                                if self.board.winner() != None:
                                    self.running = False
                                    print("Winner is: " + str(self.board.winner())) 
                                
                                print("In teriorul tablei x:" + str(board_x) + " y:" + str(board_y))
                        else:
                            print("In afara tablei")
            if self.board.getPlayer() == const.WHITE and self.running == True:          
                self.board = self.board.AIMakeMove()
                if self.board.winner() != None:
                    self.running = False
                    print("Winner is: " + str(self.board.winner())) 

            # # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(const.BACKGROUND_COLOR)

            self.drawTurnText()

            self.drawTime()

            self.drawBoard()

            pygame.display.flip()
        pygame.quit()

