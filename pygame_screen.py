import pygame

from balls import Balls

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

    def display(self, balls: Balls):
        n_balls = balls.n_balls
        for i in range(n_balls):
            pygame.draw.circle(
                self.screen,
                balls.colors[i],
                balls.positions[i],
                balls.radiuses[i],
                balls.radiuses[i] // 3,
            )
