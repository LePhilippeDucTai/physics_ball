import sys, pygame
import numpy as np
import time
from pygame_screen import RectangleScreen, BallRenderer
from ball import ball_generator

from dataclasses import dataclass

def main():

    window = RectangleScreen(400, 380)
    screen = window.make()
    ball_renderer = BallRenderer(screen)
    dt = 0.1
    n_balls = 20
    balls = [ball_generator(window, 20) for _ in range(n_balls)]

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
