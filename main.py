import sys, pygame
import time
from pygame_screen import RectangleScreen, BallRenderer
from ball import balls_generator


def main():

    window = RectangleScreen(600, 1000)
    screen = window.make()
    ball_renderer = BallRenderer(screen)
    dt = 0.1
    n_balls = 30
    gravity = 40
    balls = balls_generator(window, gravity, n_balls)
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
