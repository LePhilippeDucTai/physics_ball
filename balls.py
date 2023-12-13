import functools as ft
from dataclasses import dataclass
import random

import numpy as np


COLORS = {
    "red": (249, 13, 27),
    "orange": (254, 96, 6),
    # "yellow": (253, 224, 5),
    "phlox": (236, 0, 252),
    "violet": (157, 0, 254),
    "malachite": (0, 207, 53),
    "blue": (38, 101, 189),
    "green": (59, 188, 84),
    "cerise": (225, 45, 123),
    # "khaki": (236, 231, 136),
}
LS_COLORS = list(COLORS.values())


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
    friction: float = 0.1

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

    def update(self, dt: float):
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
    radiuses = gen.integers(10, 30, size=n_balls)
    colors = random.choices(LS_COLORS, k=n_balls)
    radiuses = gen.integers(10, 30, size=n_balls)
    bouncinesses = gen.uniform(0.8, 0.98, size=n_balls)[:, np.newaxis]
    return Balls(
        positions=positions,
        velocities=velocities,
        accelerations=accelerations,
        radiuses=radiuses,
        colors=colors,
        bouncinesses=bouncinesses,
        max_height=H,
        max_width=W,
    )
