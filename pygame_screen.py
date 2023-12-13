import pygame
import pygame.gfxdraw
from balls import Balls


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


def render_balls(screen, balls: Balls) -> list[pygame.Rect]:
    """Draws circles and returns the associated objects."""
    return [
        pygame.draw.circle(
            screen,
            balls.colors[i],
            balls.positions[i],
            balls.radiuses[i],
            balls.radiuses[i] // 3,
        )
        for i in range(balls.n_balls)
    ]


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
            balls.radiuses[i],
            balls.colors[i],
        )
        surfaces.append(surface)
    return surfaces


class BallRenderer:
    def __init__(self, screen, balls: Balls):
        self.screen = screen
        self.balls = balls
        self.n_balls = balls.n_balls
        self.rects = create_surfaces(balls)

    def update_positions(self):
        self.screen.blits(zip(self.rects, self.balls.positions))
        # for i in range(self.n_balls):
        #     # shape = self.rects[i].width, self.rects[i].height
        #     # self.rects[i].update(self.balls.positions[i], shape)
        #     self.screen.blit(self.rects[i], self.balls.positions[i])

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


# def pygame_draw_circle_generator(screen):
#     while True:
#         pygame.draw.circle(
#             screen,
#             balls.colors[i],
#             balls.positions[i],
#             balls.radiuses[i],
#             balls.radiuses[i] // 3,
#         )
