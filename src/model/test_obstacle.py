import unittest
from obstacle import Cercle, Rectangle, Ligne, Triangle

class MockRobot:
    def __init__(self, points):
        self._points = points  # Liste des points représentant la forme du robot
    
    def points(self):
        return self._points

class TestObstacle(unittest.TestCase):
    
    def test_collision_cercle(self):
        cercle = Cercle((50, 50), 10)
        self.assertTrue(cercle.detecter_collision_point((55, 50)))  # À l'intérieur
        self.assertFalse(cercle.detecter_collision_point((70, 50)))  # À l'extérieur
    
    def test_collision_cercle_robot(self):
        cercle = Cercle((50, 50), 10)
        robot = MockRobot([(55, 50), (60, 50)])  # Un point dans le cercle
        self.assertTrue(cercle.detecter_collision(robot))
    
    def test_collision_rectangle(self):
        rectangle = Rectangle((30, 30), (20, 10))
        self.assertTrue(rectangle.detecter_collision_point((35, 35)))  # À l'intérieur
        self.assertFalse(rectangle.detecter_collision_point((60, 50)))  # À l'extérieur
    
    def test_collision_rectangle_robot(self):
        rectangle = Rectangle((30, 30), (20, 10))
        robot = MockRobot([(35, 35), (40, 40)])  # Un point dans le rectangle
        self.assertTrue(rectangle.detecter_collision(robot))
    
    def test_collision_ligne(self):
        ligne = Ligne((10, 10), (20, 10), 5)
        self.assertTrue(ligne.detecter_collision_point((15, 10)))  # Sur la ligne
        self.assertFalse(ligne.detecter_collision_point((30, 30)))  # Hors ligne
    
    def test_collision_ligne_robot(self):
        ligne = Ligne((10, 10), (20, 10), 5)
        robot = MockRobot([(15, 10)])  # Un point sur la ligne
        self.assertTrue(ligne.detecter_collision(robot))
    
    def test_collision_triangle(self):
        triangle = Triangle((0, 0), (10, 0), (5, 10))
        self.assertTrue(triangle.detecter_collision_point((5, 5)))  # À l'intérieur
        self.assertFalse(triangle.detecter_collision_point((10, 10)))  # À l'extérieur
    
    def test_collision_triangle_robot(self):
        triangle = Triangle((0, 0), (10, 0), (5, 10))
        robot = MockRobot([(5, 5)])  # Un point dans le triangle
        self.assertTrue(triangle.detecter_collision(robot))

if __name__ == "__main__":
    unittest.main()
