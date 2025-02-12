import unittest
from Model.Robot import *
from Model.Obstacle import *
from Model.Environnement import *


class TestRobot(unittest.TestCase):
    
    def test_initialisation(self):
        robot = Robot(10, 20, math.pi/2, 50, 50)
        self.assertEqual(robot.x, 10)
        self.assertEqual(robot.y, 20)
        self.assertEqual(robot.direction, math.pi/2)
        self.assertEqual(robot.vitesse_gauche, 50)
        self.assertEqual(robot.vitesse_droite, 50)

    def test_avancer(self):
        robot = Robot(0, 0, 0, 50, 50)
        robot.avancer(1)
        self.assertAlmostEqual(robot.x, 50, delta=0.1)
        self.assertAlmostEqual(robot.y, 0, delta=0.1)

    def test_appliquer_vitesse_gauche(self):
        robot = Robot(0, 0)
        robot.appliquer_vitesse_gauche(30)
        self.assertEqual(robot.vitesse_gauche, 30)

    def test_appliquer_vitesse_droite(self):
        robot = Robot(0, 0)
        robot.appliquer_vitesse_droite(40)
        self.assertEqual(robot.vitesse_droite, 40)

    def test_arreter_robot(self):
        robot = Robot(0, 0, vitesse_gauche=50, vitesse_droite=50)
        robot.arreter_robot()
        self.assertEqual(robot.vitesse_gauche, 0)
        self.assertEqual(robot.vitesse_droite, 0)

    def test_cpadistance(self):
        robot = Robot(0, 0, direction=0)
        obstacle = Cercle((16, 0), 5)  # Position de l'obstacle
        env = Environnement()
        env.ajouter_obstacle(obstacle)

        detection, distance = robot.cpadistance(env)

        print(f"🛑 Debug: detection={detection}, distance={distance}")

        self.assertTrue(detection)
        self.assertAlmostEqual(distance, 12, delta=0.1)


class TestEnvironnement(unittest.TestCase):

    def test_ajouter_obstacle(self):
        env = Environnement()
        cercle = Cercle((10, 10), 5)
        env.ajouter_obstacle(cercle)
        self.assertIn(cercle, env.obstacles)

    def test_detecter_sorties(self):
        env = Environnement((0, 100), (0, 100))
        robot = Robot(150, 50)
        self.assertTrue(env.detecter_sorties(robot))


class TestObstacles(unittest.TestCase):

    def test_collision_cercle(self):
        robot = Robot(10, 10)
        cercle = Cercle((12, 10), 3)
        self.assertTrue(cercle.detecter_collision(robot))

    def test_collision_rectangle(self):
        robot = Robot(5, 5)
        rectangle = Rectangle((0, 0), (10, 10))
        self.assertTrue(rectangle.detecter_collision(robot))

    def test_collision_ligne(self):
        robot = Robot(5, 5)
        ligne = Ligne((0, 5), (10, 5), 2)
        self.assertTrue(ligne.detecter_collision(robot))

    def test_collision_triangle(self):
        robot = Robot(5, 5)
        triangle = Triangle((0, 0), (10, 0), (5, 10))
        self.assertTrue(triangle.detecter_collision(robot))


if __name__ == '__main__':
    unittest.main()

