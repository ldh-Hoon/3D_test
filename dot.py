import math

class point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def set_point(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def get_point_3d(self):
        return (self.x, self.y, self.z)
    def get_point_2d(self):
        d = (1000)/(1000 + self.z)
        return (self.x * d, self.y * d)