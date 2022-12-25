import numpy as np

G = 9.81

def update_point(point, velocity, acceleration, dt):
    velocity += acceleration * dt
    position += velocity * dt

def main():
    point = np.array([0, 0])
    velocity = np.array([1,1])
    acceleration = np.array([0, -G])

class Point:
    def __init__(self, position, velocity, acceleration):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity,dtype=float)
        self.acceleration = np.array(acceleration,dtype=float)
        self.history = []

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.history.append(self)

    def __repr__(self) -> str:
        return str(self.position)

class System:
    def __init__(self, points: np.array):
        pass
 
if __name__ == "__main__":
    p = Point([0,0], [1,1], [0, -G])
    dt = 0.01
    # for _ in range(50):
    #     p.update(dt)
    #     print(p) 
    
    x = np.array([5.1, 40.9409], dtype=float)

    print(x)
    print(x.astype(int))

   