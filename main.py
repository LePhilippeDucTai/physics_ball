import sys
import time

import pygame

from balls import balls_generator
from pygame_screen import BallRenderer, RectangleScreen


def main():
    window = RectangleScreen(1000, 1500)
    screen = window.make()
    ball_renderer = BallRenderer(screen)
    dt = 0.1
    n_balls = 50
    gravity = 0
    balls = balls_generator(window, gravity, n_balls)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        window.fill()
        balls.update(dt)
        ball_renderer.display(balls)

        pygame.display.flip()
        time.sleep(0.005)


if __name__ == "__main__":
    main()
