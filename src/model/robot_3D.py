import math

class Robot:
    def __init__(self, x, y, z=0, direction=0, vitesse_gauche=0, vitesse_droite=0, distance_roues=30, taille_robot=20, vitesse_max=200, environnement=None):
        """
        Initialise un robot différentiel en 3D avec position, direction et vitesses de roues.
        
        :param x: Position initiale en x
        :param y: Position initiale en y
        :param z: Position initiale en z (ajouté pour la 3D)
        :param direction: Direction initiale du robot (en radians, autour de l'axe vertical)
        :param vitesse_gauche: Vitesse initiale de la roue gauche (en unités par seconde)
        :param vitesse_droite: Vitesse initiale de la roue droite (en unités par seconde)
        :param distance_roues: Distance entre les roues (en unités)
        :param taille_robot: Taille du robot (utilisé pour les collisions)
        :param vitesse_max: Vitesse maximale que peut atteindre le robot
        :param environnement: Environnement dans lequel le robot évolue (obstacles, etc.)
        """
        self.x = x
        self.y = y
        self.z = z  # Ajout de la composante z pour la 3D
        self.direction = direction  # Direction en radians
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.distance_roues = distance_roues
        self.taille_robot = taille_robot
        self.vitesse_max = vitesse_max
        self.environnement = environnement

    def mise_a_jour_robot(self, dt):
        """
        Met à jour la position et la direction du robot sur une période de temps donnée.
        
        :param dt: Intervalle de temps (en secondes)
        """
        # Calcul de la vitesse linéaire et angulaire
        vitesse_lineaire = (self.vitesse_gauche + self.vitesse_droite) / 2
        vitesse_angulaire = (self.vitesse_droite - self.vitesse_gauche) / self.distance_roues

        # Mise à jour de la direction (en 3D, on peut penser à une rotation autour d'axes)
        self.direction += vitesse_angulaire * dt

        # Calcul du déplacement en x, y, z
        dx = vitesse_lineaire * math.cos(self.direction) * dt
        dy = vitesse_lineaire * math.sin(self.direction) * dt
        dz = 0  # Pas de déplacement vertical pour le moment (on peut l'ajouter si nécessaire)

        # Mise à jour de la position
        self.x += dx
        self.y += dy
        self.z += dz

    def appliquer_vitesse_gauche(self, delta_vitesse):
        """
        Modifie la vitesse de la roue gauche en ajoutant une variation de vitesse.
        
        :param delta_vitesse: Variation de la vitesse (positive ou négative)
        """
        if (delta_vitesse >= 0 and delta_vitesse < self.vitesse_max):
            self.vitesse_gauche = delta_vitesse
        if (delta_vitesse <= 0 and delta_vitesse > -self.vitesse_max):
            self.vitesse_gauche = delta_vitesse

    def appliquer_vitesse_droite(self, delta_vitesse):
        """
        Modifie la vitesse de la roue droite en ajoutant une variation de vitesse.
        
        :param delta_vitesse: Variation de la vitesse (positive ou négative)
        """
        if (delta_vitesse >= 0 and delta_vitesse < self.vitesse_max):
            self.vitesse_droite = delta_vitesse
        if (delta_vitesse <= 0 and delta_vitesse > -self.vitesse_max):
            self.vitesse_droite = delta_vitesse

    def capteurdistance(self):
        """Retourne True et la distance minimale si un obstacle est détecté par un des capteurs avant du robot, False sinon."""
        
        step = 1  # Distance entre chaque échantillon
        max_distance = 1000  # Distance maximale du capteur

        # Récupération des points du robot (en 3D)
        capteurs = self.points()  # Liste contenant les 6 points du robot
        capteur_gauche = capteurs[0]  # Point avant gauche
        capteur_droite = capteurs[1]  # Point avant droit

        distances_detectees = []

        for capteur in [capteur_gauche, capteur_droite]:
            x, y, z = capteur  # Position initiale du capteur
            current_x, current_y, current_z = x, y, z
            angle = self.direction  # Capteur aligné avec la direction du robot

            # Avancer jusqu'à la distance maximale
            for _ in range(int(max_distance / step)):
                current_x += step * math.cos(angle)
                current_y += step * math.sin(angle)

                # Vérification de collision avec les obstacles
                for obstacle in self.environnement.obstacles:
                    if obstacle.detecter_collision_point((current_x, current_y, current_z)):  # Adapté pour la 3D
                        distance = math.sqrt((current_x - x) ** 2 + (current_y - y) ** 2 + (current_z - z) ** 2)
                        distances_detectees.append(distance)
                        break  # Arrêter ce capteur après avoir détecté un obstacle

        if distances_detectees:
            return True, min(distances_detectees)  # Retourne la plus petite distance trouvée
        else:
            return False, None  # Aucun obstacle détecté

    def points(self):
        """
        Retourne les trois sommets du triangle représentant le robot, avec un point entre chaque 2 sommets.
        En 3D, on considère le robot comme un triangle mais avec des coordonnées Z également.
        """
        p1 = (self.x + self.taille_robot * math.cos(self.direction - math.pi / 2),
              self.y + self.taille_robot * math.sin(self.direction - math.pi / 2),
              self.z)  # Ajout de la composante Z
        p2 = (self.x + self.taille_robot * math.cos(self.direction + math.pi / 2),
              self.y + self.taille_robot * math.sin(self.direction + math.pi / 2),
              self.z)  # Ajout de la composante Z
        p3 = (self.x + self.taille_robot * math.cos(self.direction + math.pi),
              self.y + self.taille_robot * math.sin(self.direction + math.pi),
              self.z)  # Ajout de la composante Z

        return [p1, p2, p3, (self.x, self.y, self.z)]

def detecter_balise(self, balise):
    """
    Détecte si la balise est visible en utilisant un capteur optique sur le robot.

    :param balise: L'objet Balise que le robot essaie de détecter
    :return: True si la balise est détectée, sinon False
    """
    # Calcul de l'angle entre le robot et la balise
    delta_x = balise.x - self.x
    delta_y = balise.y - self.y
    delta_z = balise.z - self.z

    # Calcul de l'angle en 2D (on ignore la composante z pour la direction)
    angle_balise = math.atan2(delta_y, delta_x)

    # Calcul de l'angle entre la direction du robot et la balise
    angle_diff = (angle_balise - self.direction) % (2 * math.pi)
    
    # On considère que la balise est visible si l'angle est dans une certaine tolérance
    angle_tol = math.radians(10)  # Tolérance de 10 degrés
    if angle_diff <= angle_tol or (2 * math.pi - angle_diff) <= angle_tol:
        # Calcul de la distance pour vérifier la visibilité
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
        return True, distance
    return False, None

