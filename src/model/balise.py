from ursina import color

class Balise:
    def __init__(self, position, couleurs=None, forme='quad', taille=5, hauteur=0, rotation=0):
        """
        Balise rectangulaire multicolore (2x2), orientable.

        :param position: tuple (x, y)
        :param couleurs: liste de 4 couleurs dans l'ordre [haut-gauche, haut-droite, bas-gauche, bas-droite]
        :param forme: forme (non utilisé ici)
        :param taille: taille de la balise
        :param hauteur: base Y de la balise
        :param rotation: angle de rotation autour de Y (en degrés)
        """
        self.position = position
        self.forme = forme
        self.taille = taille
        self.hauteur = hauteur
        self.rotation = rotation

        if couleurs is None:
            self.couleurs = [color.yellow, color.green, color.red, color.blue]
        else:
            self.couleurs = couleurs[:4] + [color.white] * (4 - len(couleurs))
