import unittest
from environnement import Environnement

class MockRobot:
    def __init__(self, x, y, taille_robot, direction):
        self.x = x
        self.y = y
        self.taille_robot = taille_robot
        self.direction = direction
        self.vitesse_gauche = 0
        self.vitesse_droite = 0
    
    def arreter_robot(self):
        self.vitesse_gauche = 0
        self.vitesse_droite = 0
    
    def appliquer_vitesse_gauche(self, vitesse):
        self.vitesse_gauche = vitesse
    
    def appliquer_vitesse_droite(self, vitesse):
        self.vitesse_droite = vitesse
    
    def mise_a_jour_robot(self, dt):
        pass  # Simulation d'une mise à jour du robot

class MockObstacle:
    def __init__(self, position):
        self.position = position
    
    def detecter_collision(self, robot):
        return (robot.x, robot.y) == self.position

class TestEnvironnement(unittest.TestCase):
    
    def setUp(self):
        self.env = Environnement((0, 100), (0, 100))
        self.robot = MockRobot(50, 50, 10, 0)

    def test_ajouter_obstacle(self):
        obstacle = MockObstacle((30, 30))
        self.env.ajouter_obstacle(obstacle)
        self.assertIn(obstacle, self.env.obstacles)

    def test_detecter_sorties_dans_limites(self):
        self.assertFalse(self.env.detecter_sorties(self.robot))
    
    def test_detecter_sorties_hors_limites(self):
        self.robot.x = 150  # En dehors de la limite
        self.assertTrue(self.env.detecter_sorties(self.robot))
    
    def test_gerer_collisions_sans_collision(self):
        self.env.gerer_collisions(self.robot)
        self.assertEqual(self.robot.vitesse_gauche, 0)
        self.assertEqual(self.robot.vitesse_droite, 0)
    
    def test_gerer_collisions_avec_obstacle(self):
        obstacle = MockObstacle((50, 50))
        self.env.ajouter_obstacle(obstacle)
        self.env.gerer_collisions(self.robot)
        self.assertEqual(self.robot.vitesse_gauche, -5)  # Vérifier si la vitesse est ajustée
        self.assertEqual(self.robot.vitesse_droite, -5)
    
if __name__ == "__main__":
    unittest.main()
