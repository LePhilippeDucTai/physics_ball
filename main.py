import sys

import pygame
import pygame.gfxdraw
from balls import balls_generator
from constants import DT, GRAVITY, N_BALLS, N_FRAMES, SCREEN_HEIGHT, SCREEN_WIDTH
from pygame_screen import BallRenderer, RectangleScreen


def main():
    pygame.init()
    window = RectangleScreen(SCREEN_HEIGHT, SCREEN_WIDTH)
    screen = window.make()
    balls = balls_generator(window, GRAVITY, N_BALLS)
    ball_renderer = BallRenderer(screen, balls)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        window.fill()
        balls.update(DT)
        ball_renderer.update_positions()

        pygame.display.update()
        clock.tick(N_FRAMES)


if __name__ == "__main__":
    main()
