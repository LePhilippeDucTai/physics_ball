import functools as ft
from dataclasses import dataclass
import random
import itertools as it
import numpy as np


from constants import (
    FRICTION,
    LS_COLORS,
    MAX_BOUNCINESS,
    MAX_RADIUS,
    MIN_BOUNCINESS,
    MIN_RADIUS,
)


def is_close(pos_1: np.ndarray, pos_2: np.ndarray, radius_1: float, radius_2: float):
    distance = np.linalg.norm(pos_1 - pos_2, ord=2)
    r = radius_1 + radius_2 + 0.1
    return distance <= r


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
                v1, v2 = self.velocities[i], self.velocities[j]
                v1_p, v2_p = compute_collision_velocities(
                    pos_1, v1, pos_2, v2, radius_1, radius_2
                )
                self.velocities[i] = v1_p
                self.velocities[j] = v2_p

    def update(self, dt: float):
        self.collide_two(dt)
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


def compute_collision_velocities(x1, v1, x2, v2, m1=1, m2=1):
    scale = np.dot(v1 - v2, x1 - x2) / np.dot(x1 - x2, x1 - x2)
    v1_p = v1 - 2 * (m2 / (m1 + m2)) * scale * (x1 - x2)
    v2_p = v2 - 2 * (m1 / (m1 + m2)) * scale * (x2 - x1)
    return v1_p, v2_p


def balls_generator(window, gravity, n_balls):
    W, H = window.width, window.height
    gen = np.random.default_rng()
    accelerations = np.array([0, gravity])
    positions = gen.uniform([0, 0], [W, H], size=(n_balls, 2))
    velocities = gen.uniform([-W, -H], [W, H], size=(n_balls, 2))
    radiuses = gen.integers(MIN_RADIUS, MAX_RADIUS, size=n_balls)
    colors = random.choices(LS_COLORS, k=n_balls)
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
