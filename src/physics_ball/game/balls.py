import functools as ft
import itertools as it
import random
from dataclasses import dataclass
from math import pi

import numpy as np

from physics_ball.game.constants import (
    FRICTION,
    LS_COLORS,
    MAX_BOUNCINESS,
    MAX_RADIUS,
    MIN_BOUNCINESS,
    MIN_RADIUS,
    SCALE_VELOCITY,
)


def is_close(pos_1: np.ndarray, pos_2: np.ndarray, radius_1: float, radius_2: float):
    distance = np.linalg.norm(pos_1 - pos_2, ord=2)
    r = radius_1 + radius_2
    return distance <= r


def positions_correction(x1, x2, r1, r2):
    d = np.linalg.norm(x1 - x2, ord=2)
    mu = 0.5 * ((r1 + r2) / d - 1)
    u = x2 - x1
    return x1 - mu * u, x2 + mu * u


def compute_collision_velocities(x1, v1, x2, v2, m1, m2):
    u = x1 - x2
    v = u * np.dot(v1 - v2, u) / np.dot(u, u)
    v1_p = v1 - 2 * (m2 / (m1 + m2)) * v
    v2_p = v2 + 2 * (m1 / (m1 + m2)) * v
    return v1_p, v2_p


@dataclass
class Balls:
    positions: np.ndarray
    velocities: np.ndarray
    accelerations: np.ndarray
    radiuses: np.ndarray
    colors: tuple[int]
    bouncinesses: np.ndarray
    max_width: int
    max_height: int
    friction: float

    def __post_init__(self):
        self.x_limits = np.array([self.radiuses, self.max_width - self.radiuses])
        self.y_limits = np.array([self.radiuses, self.max_height - self.radiuses])

    @ft.cached_property
    def n_balls(self):
        return len(self.positions)

    def clip_positions(self):
        clip_x = self.positions[:, 0].clip(self.x_limits[0], self.x_limits[1])
        clip_y = self.positions[:, 1].clip(self.y_limits[0], self.y_limits[1])
        _positions = np.array([clip_x, clip_y]).T
        to_be_bounced = self.positions != _positions
        self.positions = _positions
        return to_be_bounced

    def apply_friction(self, to_be_bounced):
        has_moved = np.any(to_be_bounced, axis=1)
        duplicate = np.array([has_moved, has_moved]).T
        self.velocities = np.where(
            duplicate, self.velocities * (1 - self.friction), self.velocities
        )

    def collide_two(self):
        n_balls = self.n_balls
        combinations = it.combinations(range(n_balls), 2)
        for i, j in combinations:
            pos_1, radius_1 = self.positions[i], self.radiuses[i]
            pos_2, radius_2 = self.positions[j], self.radiuses[j]
            are_close = is_close(pos_1, pos_2, radius_1, radius_2)
            if are_close:
                self.positions[i], self.positions[j] = positions_correction(
                    self.positions[i], self.positions[j], radius_1, radius_2
                )
                v1_p, v2_p = compute_collision_velocities(
                    self.positions[i],
                    self.velocities[i],
                    self.positions[j],
                    self.velocities[j],
                    pi * radius_1**2,
                    pi * radius_2**2,
                )
                self.velocities[i] = v1_p * self.bouncinesses[i]
                self.velocities[j] = v2_p * self.bouncinesses[j]

    def update(self, dt: float):
        self.collide_two()
        self.velocities += self.accelerations * dt
        self.positions += self.velocities * dt
        to_be_bounced = self.clip_positions()
        self.apply_friction(to_be_bounced)
        self.bounce(to_be_bounced)

    def bounce(self, to_be_bounced):
        new = -self.velocities * self.bouncinesses
        self.velocities = np.where(to_be_bounced, new, self.velocities)

    @property
    def centered_positions(self):
        return self.positions - self.radiuses[:, np.newaxis]


def balls_generator(window, gravity, n_balls):
    W, H = window.width, window.height
    gen = np.random.default_rng()
    accelerations = np.array([0, gravity])
    positions = gen.uniform([0, 0], [W, H], size=(n_balls, 2))
    velocities = gen.normal(loc=0, scale=SCALE_VELOCITY, size=(n_balls, 2))
    radiuses = gen.integers(MIN_RADIUS, MAX_RADIUS, size=n_balls)
    colors = random.choices(LS_COLORS, k=n_balls)
    if MIN_BOUNCINESS == MAX_BOUNCINESS:
        bouncinesses = np.ones((n_balls, 1))
    else:
        bouncinesses = gen.uniform(MIN_BOUNCINESS, MAX_BOUNCINESS, size=n_balls)[
            :, np.newaxis
        ]
    return Balls(
        positions=positions,
        velocities=velocities,
        accelerations=accelerations,
        radiuses=radiuses,
        colors=colors,
        bouncinesses=bouncinesses,
        max_height=H,
        max_width=W,
        friction=FRICTION,
    )
