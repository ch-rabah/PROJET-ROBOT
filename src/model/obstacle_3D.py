import math
from vpython import vector, mag, dot

class Obstacle3D:
    def detecter_collision_point(self, point):
        pass

    def detecter_collision(self, robot):
        for p in robot.points():
            if self.detecter_collision_point(p):
                return True
        return False


class Sphere3D(Obstacle3D):
    def __init__(self, position, rayon):
        self.position = vector(*position)
        self.rayon = rayon

    def detecter_collision_point(self, point):
        return mag(point - self.position) < self.rayon


class Rectangle3D(Obstacle3D):
    def __init__(self, position, dimensions):
        self.position = vector(*position)
        self.dimensions = vector(*dimensions)

    def detecter_collision_point(self, point):
        min_corner = self.position
        max_corner = self.position + self.dimensions
        return (min_corner.x <= point.x <= max_corner.x and
                min_corner.y <= point.y <= max_corner.y and
                min_corner.z <= point.z <= max_corner.z)


class Ligne3D(Obstacle3D):
    def __init__(self, point1, point2, largeur):
        self.p1 = vector(*point1)
        self.p2 = vector(*point2)
        self.largeur = largeur

    def detecter_collision_point(self, point):
        d = self.p2 - self.p1
        if mag(d) == 0:
            return mag(point - self.p1) <= self.largeur / 2
        t = max(0, min(1, dot(point - self.p1, d) / dot(d, d)))
        proj = self.p1 + t * d
        return mag(proj - point) <= self.largeur / 2


class Triangle3D(Obstacle3D):
    def __init__(self, p1, p2, p3):
        self.p1 = vector(*p1)
        self.p2 = vector(*p2)
        self.p3 = vector(*p3)

    def detecter_collision_point(self, point):
        # Projection sur le plan XZ pour la simplification
        def signe(a, b, c):
            return (a.x - c.x) * (b.z - c.z) - (b.x - c.x) * (a.z - c.z)

        d1 = signe(point, self.p1, self.p2)
        d2 = signe(point, self.p2, self.p3)
        d3 = signe(point, self.p3, self.p1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def get_sommets(self):
        return [self.p1, self.p2, self.p3]
