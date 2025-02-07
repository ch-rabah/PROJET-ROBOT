import unittest
from Model.Robot import *

class TestRobot(unittest.TestCase):
    def test_avancer(self):
        robot = Robot(0, 0, math.pi / 2, 10, 10)
        robot.avancer(1)
        self.assertAlmostEqual(robot.x, 0, places=2)
        self.assertAlmostEqual(robot.y, 10, places=2)

    def test_appliquer_vitesse(self):
        robot = Robot(0, 0)
        robot.appliquer_vitesse_gauche(50)
        self.assertEqual(robot.vitesse_gauche, 50)
        robot.appliquer_vitesse_droite(50)
        self.assertEqual(robot.vitesse_droite, 50)

    def test_decelerer_robot(self):
        robot = Robot(0, 0, vitesse_gauche=10, vitesse_droite=10)
        robot.decelerer_robot()
        self.assertLess(robot.vitesse_gauche, 10)
        self.assertLess(robot.vitesse_droite, 10)

    def test_arreter_robot(self):
        robot = Robot(0, 0, vitesse_gauche=10, vitesse_droite=10)
        robot.arreter_robot()
        self.assertEqual(robot.vitesse_gauche, 0)
        self.assertEqual(robot.vitesse_droite, 0)

if __name__ == "__main__":
    unittest.main()

