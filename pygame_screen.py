import pygame
import pygame.gfxdraw
from balls import Balls
from constants import BACKGROUND_COLOR


class RectangleScreen:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.background_colour = BACKGROUND_COLOR

    def make(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fill()
        return self.screen

    def fill(self):
        self.screen.fill(self.background_colour)


def create_surfaces(balls: Balls) -> list[pygame.Surface]:
    """Draws circles and returns the associated surfaces."""
    surfaces = []
    for i in range(balls.n_balls):
        surface = pygame.Surface(
            (2 * balls.radiuses[i], 2 * balls.radiuses[i]), pygame.SRCALPHA
        )
        pygame.gfxdraw.filled_circle(
            surface,
            balls.radiuses[i],
            balls.radiuses[i],
            balls.radiuses[i] - 1,
            balls.colors[i],
        )
        surfaces.append(surface)
    return surfaces


class BallRenderer:
    def __init__(self, screen: pygame.Surface, balls: Balls):
        self.screen = screen
        self.balls = balls
        self.n_balls = balls.n_balls
        self.rects = create_surfaces(balls)

    def update_positions(self):
        self.screen.blits(zip(self.rects, self.balls.centered_positions))
