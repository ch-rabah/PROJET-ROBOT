import pygame

# Définition des couleurs
ROUGE = (255, 0, 0)
NOIR = (0, 0, 0)
BLUE = (0,0,255)
VERT = (0, 255, 0)
JAUNE = (255, 255, 0)
ROSE = (255, 0, 255)


# Classe mère pour les obstacles
class Obstacle:
	def __init__(self):
		"""Constructeur pour la classe Obstacle (doit être implémentée dans les sous-classes)"""
		pass # Pas de propriété commune par défaut pour les obstacles


	def dessiner(self, surface):
		"""Méthode pour dessiner l'obstacle (doit être implémentée dans les sous-classes)"""
		pass

	def est_dans(self, x, y):
		"""Méthode pour vérifier si un point (x, y) est dans l'obstacle (doit être implémentée dans les sous-classes)"""
		pass

# Classe Forme, qui hérite d'Obstacle
class Forme(Obstacle):
	def __init__(self, pos_x, pos_y):
		"""Un constructeur par défauts qui initialise une forme avec une position centrale (pos_x, pos_y) """
		self.pos_x=pos_x
		self.pos_y=pos_y
#pos_x,pos_y sont le centre de quelques formes (les formes triangle et ligne n'ont pas de centre)
	
	
	
class Ellipse(Forme):
	def __init__(self, pos_x, pos_y, grand_axe, petit_axe):
		"""
		Initialise une ellipse avec sa position et ses dimensions.
		:param pos_x: Position en X du centre.
		:param pos_y: Position en Y du centre.
		:param grand_axe: Longueur du grand axe.
		:param petit_axe: Longueur du petit axe.
		"""
		super().__init__(pos_x, pos_y)
		self.grand_axe = grand_axe
		self.petit_axe = petit_axe
        		
	def dessiner(self, ecran):
        	pygame.draw.ellipse(ecran, ROUGE, (self.pos_x - self.grand_axe/2 , self.pos_y - self.petit_axe/2, self.grand_axe,self.petit_axe ))
        
	def est_dans(self, x, y):
		return (((x - self.pos_x) ** 2) / ((self.grand_axe / 2) ** 2) + ((y - self.pos_y) ** 2) / ((self.petit_axe / 2) ** 2)) <= 1


		
class Rectangle(Forme):
	def __init__(self, pos_x, pos_y, largeur, hauteur):
		"""
		Initialise un rectangle avec sa position et ses dimensions.
		:param pos_x: Position en X du centre.
		:param pos_y: Position en Y du centre.
		:param largeur: Largeur du rectangle.
		:param hauteur: Hauteur du rectangle.
		"""
		super().__init__(pos_x, pos_y)
		self.largeur = largeur
		self.hauteur = hauteur

	def est_dans(self, x, y):
		return (self.pos_x - self.largeur/2 <= x <= self.pos_x + self.largeur/2 and self.pos_y - self.hauteur/2 <= y <= self.pos_y + self.hauteur/2)

	def dessiner(self, surface):
		pygame.draw.rect(surface, BLUE, (self.pos_x - self.largeur/2, self.pos_y - self.hauteur/2, self.largeur, self.hauteur))



class Triangle(Forme):

	def __init__(self, sommet1, sommet2, sommet3):
		"""
		Initialise un triangle avec ses trois sommets.
		:param sommet1: Tuple (x, y) du premier sommet.
		:param sommet2: Tuple (x, y) du deuxième sommet.
		:param sommet3: Tuple (x, y) du troisième sommet.
		"""
		self.sommet1 = sommet1
		self.sommet2 = sommet2
		self.sommet3 = sommet3

	def est_dans(self, x, y):
		x1, y1 = self.sommet1
		x2, y2 = self.sommet2
		x3, y3 = self.sommet3
		
		def aire(x1, y1, x2, y2, x3, y3):
			"""Calcule l'aire d'un triangle défini par trois points."""
			return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)
			
		aire_total = aire(x1, y1, x2, y2, x3, y3)
		aire1 = aire(x, y, x2, y2, x3, y3)
		aire2 = aire(x1, y1, x, y, x3, y3)
		aire3 = aire(x1, y1, x2, y2, x, y)
		return aire_total == aire1 + aire2 + aire3

	def dessiner(self, surface):
		pygame.draw.polygon(surface, VERT, [self.sommet1, self.sommet2, self.sommet3])
        	
class Ligne(Forme):

	def __init__(self, point1, point2):
		"""
		Initialise une ligne entre deux points.
		:param point1: Tuple (x, y) du premier point.
		:param point2: Tuple (x, y) du deuxième point.
		"""
		self.point1 = point1
		self.point2 = point2

	def est_dans(self, x, y):
		x1, y1 = self.point1
		x2, y2 = self.point2

		# Calculer la distance entre le point et la ligne
		if x1 == x2:  # Cas d'une ligne verticale
			return abs(x - x1) < 2  # On vérifie si x est proche de la ligne (largeur de 2 pixels)
		if y1 == y2:  # Cas d'une ligne horizontale
			return abs(y - y1) < 2  # Idem pour y
		# Équation de la ligne : y = mx + b
		m = (y2 - y1) / (x2 - x1)
		b = y1 - m * x1
		y_calculé = m * x + b

		# Vérifie si le point est proche de la ligne (tolérance de 2 pixels)
		return abs(y - y_calculé) < 2

	def dessiner(self, ecran):
		pygame.draw.line(ecran, JAUNE, self.point1, self.point2, 2)  # Dessiner une ligne de 2 pixels d'épaisseur


#Tests et Affichages
pygame.init()
largeur, hauteur = 800, 600
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Test des Formes")


# Création des formes
formes = [
        Ellipse(200, 150, 100, 50),
        Rectangle(400, 300, 120, 80),
        Triangle((600, 100), (550, 200), (650, 200)),
        Ligne((100, 500), (300, 550))
    ]
    
# Points à tester
points_a_tester = [
    (200, 150), (250, 160),  # Points pour l'ellipse
    (400, 300), (500, 320),  # Points pour le rectangle
    (600, 150), (550, 180),  # Points pour le triangle
    (100, 500), (220, 540)   # Points pour la ligne
]

# Teste les points 
for point in points_a_tester:
		x, y = point
		for forme in formes:
			if forme.est_dans(x, y):
				print(f"Le point {point} est dans la forme {type(forme).__name__}")
			else:
				print(f"Le point {point} n'est pas dans la forme {type(forme).__name__}")
		print(f"**********************************************************")

# Boucle principale
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Efface l'écran
	ecran.fill(NOIR)

	# Dessine toutes les formes
	for forme in formes:
		forme.dessiner(ecran)
	
	# Affiche les ponts en rose
	for point in points_a_tester:
		x, y = point
		pygame.draw.circle(ecran, ROSE, (x, y), 2)

	# Met à jour l'affichage
	pygame.display.flip()

pygame.quit()

