import math

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
    
    def detecter_collision(self, robot):
        """
        Vérifie si le robot entre en collision avec le cercle.
        Retourne (collision: bool, arriere: bool, lateral: bool).
        """
        cx, cy = self.position
        for px, py in robot.points():
            distance = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
            if distance < self.rayon:
                return (True)
        return (False)
    

class Rectangle(Obstacle):
    def __init__(self, position, dimensions):
        """
		Initialise un rectangle avec sa position et ses dimensions (hauteurs et longeur).
		:param position: Position en (X, Y).		
		:param dimensions: dimensions de rectangle (hauteurs et longeur).
		"""
        self.position=position
        self.dimensions=dimensions
    
    def detecter_collision(self, robot):
        """
        Vérifie si le robot entre en collision avec le rectangle.
        Retourne (collision: bool, arriere: bool, lateral: bool).
        """
        rx, ry = self.position
        largeur, hauteur= self.dimensions
        for px, py in robot.points():
            if rx <= px <= rx + largeur and ry <= py <= ry + hauteur:
                return (True)
        return (False)