import pygame

pygame.init()

class RectangleScreen:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.background_colour = (230, 230, 230)

    def make(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fill()
        return self.screen

    def fill(self):
        self.screen.fill(self.background_colour)

class BallRenderer:
    def __init__(self, screen):
        self.screen = screen

    def display(self, ball):
        pygame.draw.circle(
            self.screen,
            ball.color,
            ball.position,
            ball.radius,
            ball.radius,
        )
