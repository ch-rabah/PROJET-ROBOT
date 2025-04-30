class Balise:
    def __init__(self, position, couleur, forme='cube', taille=5, hauteur=0):
        """
        Initialise une balise colorée.

        :param position: tuple (x, y) représentant la position dans l'environnement (2D)
        :param couleur: couleur de la balise (nom de couleur Ursina, ex: 'red', 'blue', etc.)
        :param forme: modèle Ursina à utiliser (par défaut 'cube')
        :param taille: taille de la balise
        :param hauteur: hauteur d'élévation dans la scène (axe Y)
        """
        self.position = position
        self.couleur = couleur
        self.forme = forme
        self.taille = taille
        self.hauteur = hauteur
