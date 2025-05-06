import unittest
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.abspath(os.path.join(THIS_DIR, os.pardir))

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from FWSFR.model.robot import Robot

class MockEnvironnement:
    def __init__(self, obstacles=None):
        self.obstacles = obstacles if obstacles else []

class TestRobot(unittest.TestCase):
    
    def setUp(self):
        self.env = MockEnvironnement()
        self.robot = Robot(50, 50, direction=0, environnement=self.env)

    def test_mise_a_jour_robot(self):
        self.robot.vitesse_gauche = 10
        self.robot.vitesse_droite = 10
        self.robot.mise_a_jour_robot(1)
        self.assertNotEqual((self.robot.x, self.robot.y), (50, 50))  # Le robot doit se déplacer
    
    def test_appliquer_vitesse_gauche(self):
        self.robot.appliquer_vitesse_gauche(50)
        self.assertEqual(self.robot.vitesse_gauche, 50)
        self.robot.appliquer_vitesse_gauche(-50)
        self.assertEqual(self.robot.vitesse_gauche, -50)
    
    def test_appliquer_vitesse_droite(self):
        self.robot.appliquer_vitesse_droite(50)
        self.assertEqual(self.robot.vitesse_droite, 50)
        self.robot.appliquer_vitesse_droite(-50)
        self.assertEqual(self.robot.vitesse_droite, -50)
    
    def test_arreter_robot(self):
        self.robot.vitesse_gauche = 30
        self.robot.vitesse_droite = 30
        self.robot.arreter_robot()
        self.assertEqual(self.robot.vitesse_gauche, 0)
        self.assertEqual(self.robot.vitesse_droite, 0)
    
if __name__ == "__main__":
    unittest.main()