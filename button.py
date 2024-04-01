import pygame
import constants as const


class Button():
    def __init__(self, x_pos, y_pos, width, height, text_input, screen, main_font):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.screen = screen
        self.main_font = main_font
        self.rect = pygame.Rect(x_pos, y_pos, width, height)
        self.text_input = text_input
        self.text = self.main_font.render(self.text_input, True, const.BACKGROUND_COLOR)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(self.screen, const.LINE_COLOR, self.rect)  # Draw button rectangle
        self.screen.blit(self.text, self.text_rect)  # Draw text

    def pressed(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.main_font.render(self.text_input, True, "green")
        else:
            self.text = self.main_font.render(self.text_input, True, const.LINE_COLOR)
