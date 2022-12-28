from dataclasses import dataclass
import numpy as np
from pygame_screen import RectangleScreen


@dataclass
class Ball:
    position: np.array
    velocity: np.array
    acceleration: np.array
    radius: float
    color: tuple[int]
    bounciness: float
    friction: float = 0.01

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
        if y <= r or H - y <= r or x <= r or x >= W - r:
            self.velocity *= 1 - self.friction
        if y < r or H - y < r:
            self.velocity *= self.floor_bounce()
            self.position[1] = r if y < r else H - r
        if x < r or x > W - r:
            self.velocity *= self.side_bounce()
            self.position[0] = r if x < r else W - r


def ball_generator(screen, gravity):
    W, H = screen.width, screen.height
    gen = np.random.default_rng()
    acceleration = np.array([0, gravity])
    position = gen.uniform([0, 0], [H, W], size=2)
    velocity = gen.uniform([0, 0], [H, W], size=2)
    color = gen.integers(low=0, high=125, size=4)
    radius = gen.integers(10, 30)
    bounciness = gen.uniform(0.8, 0.98)
    return Ball(position, velocity, acceleration, radius, color, bounciness)


def balls_generator(window, gravity, n_balls):
    return [ball_generator(window, gravity) for _ in range(n_balls)]
