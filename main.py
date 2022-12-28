import sys, pygame
import numpy as np
import time
import cmath, math

from dataclasses import dataclass

pygame.init()


class RectangleScreen:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.background_colour = (255, 255, 255)

    def make(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fill()
        return self.screen

    def fill(self):
        self.screen.fill(self.background_colour)


@dataclass
class Ball:
    position: np.array
    velocity: np.array
    acceleration: np.array
    radius: float
    color: tuple[int]
    bounciness: float

    def update(self, screen, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.bounce(screen)

    def side_bounce(self):
        return np.array([-self.bounciness, 1])

    def floor_bounce(self):
        return np.array([1, -self.bounciness])

    def bounce(self, rect_screen: RectangleScreen):
        x, y = self.position
        W, H = rect_screen.width, rect_screen.height
        r = self.radius
        if y < r or H - y < r:
            self.velocity *= self.floor_bounce()
            self.position[1] = r if y < r else H - r
        if x < r or x > W - r:
            self.velocity *= self.side_bounce()
            self.position[0] = r if x < r else W - r


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


def ball_generator(screen, gravity):
    W, H = screen.width, screen.height
    gen = np.random.default_rng()
    acceleration = np.array([0, gravity])
    position = gen.uniform([0, 0], [H, W], size=2)
    velocity = gen.uniform([0, 0], [H, W], size=2)
    color = gen.integers(low=0, high=256, size=3)
    radius = gen.integers(10, 20)
    bounciness = gen.uniform(0.7, 0.95)
    return Ball(position, velocity, acceleration, radius, color, bounciness)


def main():
    dt = 0.1
    n_balls = 20
    window = RectangleScreen(400, 380)
    screen = window.make()
    balls = [ball_generator(window, 20) for _ in range(n_balls)]
    ball_renderer = BallRenderer(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        window.fill()
        for ball in balls:
            ball.update(window, dt)
            ball_renderer.display(ball)

        pygame.display.flip()
        time.sleep(0.01)


if __name__ == "__main__":
    main()
