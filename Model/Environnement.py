import math
import unittest

class Robot:
    def __init__(self, x, y, direction=0, vitesse_gauche=0, vitesse_droite=0, distance_roues=30, taille_robot=20, vitesse_max=200):
        self.x = x
        self.y = y
        self.direction = direction
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.distance_roues = distance_roues
        self.taille_robot = taille_robot
        self.vitesse_max = vitesse_max

    def avancer(self, dt):
        vitesse_lineaire = (self.vitesse_gauche + self.vitesse_droite) / 2
        vitesse_angulaire = (self.vitesse_droite - self.vitesse_gauche) / self.distance_roues
        self.direction += vitesse_angulaire * dt
        self.x += vitesse_lineaire * math.cos(self.direction) * dt
        self.y += vitesse_lineaire * math.sin(self.direction) * dt

    def appliquer_vitesse_gauche(self, delta_vitesse):
        v = self.vitesse_gauche
        if -self.vitesse_max < v + delta_vitesse < self.vitesse_max:
            self.vitesse_gauche += delta_vitesse

    def appliquer_vitesse_droite(self, delta_vitesse):
        v = self.vitesse_droite
        if -self.vitesse_max < v + delta_vitesse < self.vitesse_max:
            self.vitesse_droite += delta_vitesse

    def decelerer_robot(self):
        if self.vitesse_droite != 0:
            self.appliquer_vitesse_droite(-2 if self.vitesse_droite > 0 else 2)
        if self.vitesse_gauche != 0:
            self.appliquer_vitesse_gauche(-2 if self.vitesse_gauche > 0 else 2)

    def arreter_robot(self):
        self.vitesse_droite = 0
        self.vitesse_gauche = 0

    def cpadistance(self, environnement):
        angle = self.direction
        step = 1
        max_distance = 1000
        x, y = self.x, self.y
        current_x, current_y = x, y

        for _ in range(int(max_distance / step)):
            current_x += step * math.cos(angle)
            current_y += step * math.sin(angle)
            test_robot = Robot(current_x, current_y, direction=self.direction, taille_robot=self.taille_robot)
            for obstacle in environnement.obstacles:
                collision = obstacle.detecter_collision(test_robot)
                if collision[0]:
                    distance = math.sqrt((current_x - x) ** 2 + (current_y - y) ** 2)
                    return True, distance
        return False, None

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

