import pygame
from settings import screen
pygame.init()


class Button:
    """Button with text, action to do"""

    def __init__(self, width, height, text):
        self.width = width
        self.height = height
        self.text = text
        self.active_color = (0, 255, 64)
        self.inactive_color = (0, 0, 0)

    @staticmethod
    def new(width, height, text):
        """Creates new button"""
        return Button(width,  height, text)

    def draw(self, pos, action=None, flag=None):
        """Draw button and run the given function"""
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if pos[0] < mouse[0] < pos[0] + self.width and pos[1] < mouse[1] < pos[1] + self.height:
            pygame.draw.rect(screen, self.active_color,
                             (pos[0], pos[1], self.width, self.height))
            if click[0] == 1:
                if flag:
                    flag = False
                if action:
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_color,
                             (pos[0], pos[1], self.width, self.height))
        print_txt(self.text, "white", (pos[0] + 10, pos[1] + 10))
        return flag


def print_txt(message, color, place):
    """print text in chosen place"""
    game_font = pygame.font.Font(None, 50)
    text = game_font.render(message, True, color)
    screen.blit(text, place)
