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
    
    def detecter_collision_point(self, point):
        """
        Vérifie si un point entre en collision avec le cercle.
        Retourne True si une collision est détectée, sinon False.
        """
        cx, cy = self.position  # Centre du cercle

        def point_dans_cercle(px, py):
            """Vérifie si un point (px, py) est à l'intérieur du cercle."""
            distance = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
            return distance < self.rayon

        return point_dans_cercle(point[0], point[1])
    
    def detecter_collision(self, robot):
        """
        Vérifie si un robot entre en collision avec le rectangle.
        Retourne True si une collision est détectée, sinon False.
        """
        for  p in robot.points():
                if self.detecter_collision_point(p):
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
    
    def detecter_collision_point(self, point):
        """
        Vérifie si un point entre en collision avec le rectangle.
        Retourne True si une collision est détectée, sinon False.
        """
        rx, ry = self.position
        largeur, hauteur = self.dimensions

        def point_dans_rectangle(px, py):
            """Vérifie si un point (px, py) est dans le rectangle."""
            return rx <= px <= rx + largeur and ry <= py <= ry + hauteur

        px, py=point

        
        return point_dans_rectangle(px, py)
            
    
    def detecter_collision(self, robot):
        """
        Vérifie si un robot entre en collision avec le rectangle.
        Retourne True si une collision est détectée, sinon False.
        """
        for  p in robot.points():
                if self.detecter_collision_point(p):
                    return True

        return False
        
class Ligne:
    def __init__(self, point1, point2, largeur):
        self.point1 = point1
        self.point2 = point2
        self.largeur = largeur
        self.position = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)  # Milieu de la ligne

    def detecter_collision(self, robot):
        x1, y1 = self.point1
        x2, y2 = self.point2
        
        for px, py in robot.points():
            dx, dy = x2 - x1, y2 - y1
            longueur = math.sqrt(dx**2 + dy**2)
            if longueur == 0:
                continue
            t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (longueur**2)))
            proj_x, proj_y = x1 + t * dx, y1 + t * dy
            distance = math.sqrt((proj_x - px) ** 2 + (proj_y - py) ** 2)
            if distance <= self.largeur / 2:
                return True
        return False

    
class Triangle:
    def __init__(self, point1, point2, point3):
        self.sommets = [point1, point2, point3]
        self.position = ((point1[0] + point2[0] + point3[0]) / 3, (point1[1] + point2[1] + point3[1]) / 3)

    def detecter_collision(self, robot):
        def signe(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        for px, py in robot.points():
            d1 = signe((px, py), self.sommets[0], self.sommets[1])
            d2 = signe((px, py), self.sommets[1], self.sommets[2])
            d3 = signe((px, py), self.sommets[2], self.sommets[0])
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            if not (has_neg and has_pos):
                return True
        return False

    def get_sommets(self):
        return self.sommets



