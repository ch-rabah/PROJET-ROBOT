import math

class Obstacle:
    def __init__(self, type_forme, position, dimensions):
        """
        Crée un obstacle avec un type de forme, une position et des dimensions spécifiques.
        
        :param type_forme: Type de la forme ('rectangle', 'cercle', etc.)
        :param position: Position de l'obstacle sous forme (x, y)
        :param dimensions: Liste de dimensions adaptées à chaque forme (par exemple, [largeur, hauteur] pour un rectangle)
        """
        self.type_forme = type_forme
        self.position = position
        self.dimensions = dimensions

    def detecter_collision(self, robot):
        """
        Vérifie si l'obstacle entre en collision avec le robot (considéré comme un triangle)
        Elle retourne un couple de booléen le premier indique si le robot entre en collision avec l'obstacle l'autre indique si la collision est avec la partie arriére de l'obstacle
        """
        # Récupérer les sommets du triangle du robot
        x, y = robot.x, robot.y
        direction = robot.direction
        taille_triangle = robot.taille_robot

        point1 = (
            x + taille_triangle * math.cos(direction - math.pi / 2),
            y + taille_triangle * math.sin(direction - math.pi / 2)
        )
        point2 = (
            x + taille_triangle * math.cos(direction + math.pi / 2),
            y + taille_triangle * math.sin(direction + math.pi / 2)
        )
        point3 = (
            x + taille_triangle * math.cos(direction + math.pi),
            y + taille_triangle * math.sin(direction + math.pi)
        )

        triangle_points = [point1, point2, point3, (x, y)]

        if self.type_forme == "rectangle":
            rect_x, rect_y = self.position
            rect_w, rect_h = self.dimensions

            # Vérifier si un sommet du triangle est à l'intérieur du rectangle
            for px, py in triangle_points:
                if rect_x <= px <= rect_x + rect_w and rect_y <= py <= rect_y + rect_h:
                    return (True,(px,py)==point3)

            return (False,False)  # Aucun sommet du triangle à l'intérieur du rectangle

        elif self.type_forme == "cercle":
            cercle_x, cercle_y = self.position
            rayon = self.dimensions[0]

            # Vérifier si un sommet du triangle est à l'intérieur du cercle
            for px, py in triangle_points:
                if math.sqrt((px - cercle_x) ** 2 + (py - cercle_y) ** 2) < rayon:
                    return (True,(px,py)==point3)

            return (False,False)  # Aucun sommet du triangle à l'intérieur du cercle

        return (False,False)  # Aucun type d'obstacle reconnu

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
        Vérifie si l'obstacle(cercle) entre en collision avec le robot (considéré comme un triangle)
        Elle retourne un couple de booléen le premier indique si le robot entre en collision avec l'obstacle l'autre indique si la collision est avec la partie arriére de robot
        """
        # Récupérer les sommets du triangle du robot
        x, y = robot.x, robot.y
        direction = robot.direction
        taille_triangle = robot.taille_robot

        point1 = (
            x + taille_triangle * math.cos(direction - math.pi / 2),
            y + taille_triangle * math.sin(direction - math.pi / 2)
        )
        point2 = (
            x + taille_triangle * math.cos(direction + math.pi / 2),
            y + taille_triangle * math.sin(direction + math.pi / 2)
        )
        point3 = (
            x + taille_triangle * math.cos(direction + math.pi),
            y + taille_triangle * math.sin(direction + math.pi)
        )

        triangle_points = [point1, point2, point3, (x, y)]
        cercle_x, cercle_y = self.position
        rayon = self.rayon

        # Vérifier si un sommet du triangle est à l'intérieur du cercle
        for px, py in triangle_points:
            if math.sqrt((px - cercle_x) ** 2 + (py - cercle_y) ** 2) < rayon:
                return (True,(px,py)==point3)

        return (False,False)  # Aucun sommet du triangle à l'intérieur du cercle
