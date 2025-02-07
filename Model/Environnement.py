import math
import unittest

class Environnement:
    def __init__(self,dimX= None,dimY= None):
        self.obstacles = []  # Liste d'objets Obstacle stockés dans l'environnement
        self.dimensions_x = dimX  # Largeur totale du monde
        self.dimensions_y = dimY  # Hauteur totale du monde
    
    def ajouter_obstacle(self, obstacle):
        """Ajoute un obstacle à l'environnement"""
        self.obstacles.append(obstacle)

    def detecter_sorties(self, robot):
        """
        Vérifie si le robot est en dehors des limites du monde.
        Si oui, retourne True pour indiquer une sortie.
        Sinon, retourne False.
        """
        # Position et taille du robot
        rx = robot.x
        ry = robot.y
        taille_robot = robot.taille_robot
        base_triangle = robot.taille_robot
        direction = robot.direction
        point1 = (
            rx + base_triangle * math.cos(direction - math.pi / 2),
            ry + base_triangle * math.sin(direction - math.pi / 2)
        )
        point2 = (
            rx + base_triangle * math.cos(direction + math.pi / 2),
            ry + base_triangle * math.sin(direction + math.pi / 2)
        )
        point3 = (
            rx + taille_robot * math.cos(direction + math.pi),
            ry + taille_robot * math.sin(direction + math.pi)
        )
        
        

        # Dimensions du monde
        min_x, max_x = self.dimensions_x
        min_y, max_y = self.dimensions_y

        # Vérifier si le robot est en dehors des limites du monde
        for x, y in [point1, point2, point3, (rx, ry)]:
            if x  < min_x or x  > max_x or y  < min_y or y  > max_y:
                    return True
        return False


class TestEnvironnement(unittest.TestCase):
    def test_ajouter_obstacle(self):
        env = Environnement(0, 10)
        obstacle = "ObstacleTest"
        env.ajouter_obstacle(obstacle)
        self.assertIn(obstacle, env.obstacles)

    def test_detecter_sorties(self):
        env = Environnement((0, 10), (0, 10))
        robot = type('', (), {"x": 5, "y": 5, "taille_robot": 2, "direction": 0})()
        self.assertFalse(env.detecter_sorties(robot))
        
        robot = type('', (), {"x": 11, "y": 5, "taille_robot": 2, "direction": 0})()
        self.assertTrue(env.detecter_sorties(robot))
        
        robot = type('', (), {"x": 5, "y": -1, "taille_robot": 2, "direction": 0})()
        self.assertTrue(env.detecter_sorties(robot))

if __name__ == "__main__":
    unittest.main()






