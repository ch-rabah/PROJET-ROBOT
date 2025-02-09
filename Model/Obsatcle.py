import math
import unittest
class Obstacle:
    def __init__(self):
        """
        Crée un obstacle avec un type de forme, une position et des dimensions spécifiques.
        Constructeur pour la classe Obstacle (doit être implémentée dans les sous-classes)
        """
        pass # Pas de propriété commune par défaut pour les obstacles

    def detecter_collision(self, robot):
        """
        Vérifie si l'obstacle entre en collision avec le robot (considéré comme un triangle)
        Elle retourne un couple de booléen le premier indique si le robot entre en collision avec l'obstacle l'autre indique si la collision est avec la partie arriére de l'obstacle
        (doit être implémentée dans les sous-classes)
        """
        pass # Pas de propriété commune par défaut pour les obstacles

class Cercle(Obstacle):
    def __init__(self, position, rayon):
        """
		Initialise un cercle avec sa position et son rayon.
		:param position: Position en (X, Y) du centre.		
		:param rayon: Rayon du cercle.
		"""
        self.position=position
        self.rayon=rayon
    
    def detecter_collision(self, entity):
        """
        Vérifie si une entité entre en collision avec le cercle.
        L'entité peut être :
        - Un robot (vérification sur ses points)
        - Un tuple (x, y) représentant un point.

        Retourne True si une collision est détectée, sinon False.
        """
        cx, cy = self.position  # Centre du cercle

        def point_dans_cercle(px, py):
            """Vérifie si un point (px, py) est à l'intérieur du cercle."""
            distance = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
            return distance < self.rayon

        # Si l'entité est un point (x, y) sous forme de tuple
        if isinstance(entity, tuple) and len(entity) == 2:
            return point_dans_cercle(entity[0], entity[1])
        
        # Si l'entité est un robot, vérifier tous ses points
        else:
            for px, py in entity.points():
                if point_dans_cercle(px, py):
                    return True

        return False
    

class Rectangle(Obstacle):
    def __init__(self, position, dimensions):
        """
		Initialise un rectangle avec sa position et ses dimensions (hauteurs et longeur).
		:param position: Position en (X, Y).		
		:param dimensions: dimensions de rectangle (hauteurs et longeur).
		"""
        self.position=position
        self.dimensions=dimensions
    
    def detecter_collision(self, entity):
        """
        Vérifie si une entité entre en collision avec le rectangle.
        L'entité peut être :
        - Un robot (vérification sur ses points)
        - Un tuple (x, y) représentant un point.

        Retourne True si une collision est détectée, sinon False.
        """
        rx, ry = self.position
        largeur, hauteur = self.dimensions

        def point_dans_rectangle(px, py):
            """Vérifie si un point (px, py) est dans le rectangle."""
            return rx <= px <= rx + largeur and ry <= py <= ry + hauteur

        # Si l'entité est un point (x, y) sous forme de tuple
        if isinstance(entity, tuple) and len(entity) == 2:
            return point_dans_rectangle(entity[0], entity[1])
        
        # Si l'entité est un robot, vérifier tous ses points
        else:
            for px, py in entity.points():
                if point_dans_rectangle(px, py):
                    return True

        

            return False
        
class Ligne(Obstacle):
    def __init__(self, point1, point2, epaisseur=1):
        """
        Initialise une ligne avec deux points et une épaisseur.
        :param point1: Premier point (x, y)
        :param point2: Deuxième point (x, y)
        :param epaisseur: Épaisseur de la ligne
        """
        self.point1 = point1
        self.point2 = point2
        self.epaisseur = epaisseur
    
    def detecter_collision(self, robot):
        """
        Vérifie si le robot entre en collision avec la ligne.
        Retourne (collision: bool, arriere: bool, lateral: bool).
        """
        x1, y1 = self.point1
        x2, y2 = self.point2

        for px, py in robot.points():
            dist = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            if dist <= self.epaisseur / 2:
                return True
        return False
    
class Triangle(Obstacle):
    def __init__(self, point1, point2, point3):
        """
        Initialise un triangle avec trois points.
        :param point1: Premier sommet (x, y)
        :param point2: Deuxième sommet (x, y)
        :param point3: Troisième sommet (x, y)
        """
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
    
    def point_dans_triangle(self, px, py):
        """
        Vérifie si un point est à l'intérieur du triangle en utilisant la méthode des barycentriques.
        """
        x1, y1 = self.point1
        x2, y2 = self.point2
        x3, y3 = self.point3

        detT = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        alpha = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / detT
        beta = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / detT
        gamma = 1 - alpha - beta

        return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1
    
    def detecter_collision(self, robot):
        """
        Vérifie si le robot entre en collision avec le triangle.
        Retourne (collision: bool, arriere: bool, lateral: bool).
        """
        for px, py in robot.points():
            if self.point_dans_triangle(px, py):
                return True
        return False

def test_cercle_collision():
    cercle = Cercle((5, 5), 3)
    robot = Robot(5, 5)
    assert cercle.detecter_collision(robot) == True  # Le robot est au centre du cercle

    robot = Robot(10, 10)
    assert cercle.detecter_collision(robot) == False  # Le robot est loin du cercle


def test_rectangle_collision():
    rectangle = Rectangle((2, 2), (4, 6))
    robot = Robot(3, 3)
    assert rectangle.detecter_collision(robot) == True  # Robot dans le rectangle

    robot = Robot(10, 10)
    assert rectangle.detecter_collision(robot) == False  # Robot en dehors du rectangle


def test_ligne_collision():
    ligne = Ligne((0, 0), (10, 0), epaisseur=2)
    robot = Robot(5, 1)
    assert ligne.detecter_collision(robot) == True  # Robot proche de la ligne

    robot = Robot(5, 5)
    assert ligne.detecter_collision(robot) == False  # Robot loin de la ligne


def test_triangle_collision():
    triangle = Triangle((0, 0), (5, 5), (10, 0))
    robot = Robot(5, 2)
    assert triangle.detecter_collision(robot) == True  # Robot dans le triangle

    robot = Robot(10, 10)
    assert triangle.detecter_collision(robot) == False  # Robot en dehors du triangle


def test_point_dans_triangle():
    triangle = Triangle((0, 0), (5, 5), (10, 0))
    assert triangle.point_dans_triangle(5, 2) == True  # Point à l'intérieur
    assert triangle.point_dans_triangle(10, 10) == False  # Point à l'extérieur

# Exécution des tests
if __name__ == "__main__":
    test_cercle_collision()
    test_rectangle_collision()
    test_ligne_collision()
    test_triangle_collision()
    test_point_dans_triangle()
    print("Tous les tests sont passés avec succès.")

