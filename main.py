import sys
import time

import pygame
import pygame.gfxdraw
from balls import balls_generator
from pygame_screen import BallRenderer, RectangleScreen


def main():
    pygame.init()
    window = RectangleScreen(750, 1000)
    screen = window.make()

    dt = 0.05
    n_balls = 100
    gravity = 20
    balls = balls_generator(window, gravity, n_balls)
    ball_renderer = BallRenderer(screen, balls)
    clock = pygame.time.Clock()  # get a pygame clock object
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        window.fill()
        balls.update(dt)
        ball_renderer.update_positions()

        # pygame.display.flip()
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
