import sys, pygame
import numpy as np

pygame.init()

size = width, height = 640, 480
speed = np.array([1, 1], dtype=float)
black = 0, 0, 0

gravity = 9.81
dt = 0.01
acceleration = np.array([0, gravity], dtype=float)

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    speed = speed + acceleration * dt
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    # print(speed, ballrect.x, ballrect.y)
    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()
