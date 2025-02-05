import math


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


    def detecter_sorties2(self, robot):
        """
        Vérifie si le robot est en dehors des limites du monde.
        Si oui, retourne True pour indiquer une sortie.
        Sinon, retourne False.
        """
        # Position et taille du robot
        x = robot.x
        y = robot.y
        taille_robot = robot.taille_robot

        # Dimensions du monde
        min_x, max_x = self.dimensions_x
        min_y, max_y = self.dimensions_y

        # Vérifier si le robot est en dehors des limites du monde
        return (
            x - taille_robot < min_x or
            x + taille_robot > max_x or
            y - taille_robot < min_y or
            y + taille_robot > max_y
        )
