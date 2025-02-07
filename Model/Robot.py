import math


class Robot:
    def __init__(self, x, y, direction=0, vitesse_gauche=0, vitesse_droite=0, distance_roues=30,taille_robot=20,vitesse_max=200):
        """
        Initialise un robot différentiel avec position, direction, et vitesses de roues.
        
        :param x: Position initiale en x
        :param y: Position initiale en y
        :param direction: Direction initiale du robot (en radians)
        :param vitesse_gauche: Vitesse initiale de la roue gauche (en unités par seconde)
        :param vitesse_droite: Vitesse initiale de la roue droite (en unités par seconde)
        :param distance_roues: Distance entre les roues (en unités)
        :param taille_robot: Taille du robot (utilisé pour les collisions)
        :param vitesse_max: Vitesse maximale que peut atteindre le robot

        """
        self.x = x
        self.y = y
        self.direction = direction  # Direction en radians
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.distance_roues = distance_roues
        self.taille_robot = taille_robot
        self.vitesse_max = vitesse_max

    def avancer(self, dt):
        """
        Met à jour la position et la direction du robot sur une période de temps donnée.
        
        :param dt: Intervalle de temps (en secondes)
        """
        # Calcul de la vitesse linéaire et angulaire
        vitesse_lineaire = (self.vitesse_gauche + self.vitesse_droite) / 2
        vitesse_angulaire = (self.vitesse_droite - self.vitesse_gauche) / self.distance_roues

        # Mise à jour de la direction
        self.direction += vitesse_angulaire * dt

        # Calcul du déplacement en x et y
        dx = vitesse_lineaire * math.cos(self.direction) * dt
        dy = vitesse_lineaire * math.sin(self.direction) * dt

        # Mise à jour de la position
        self.x += dx
        self.y += dy


    def appliquer_vitesse_gauche(self, delta_vitesse):
        """
        Modifie la vitesse de la roue gauche en ajoutant une variation de vitesse.
        
        :param delta_vitesse: Variation de la vitesse (positive ou négative)
        """
        v = self.vitesse_gauche
        if (delta_vitesse > 0 and v + delta_vitesse < self.vitesse_max):
            self.vitesse_gauche += delta_vitesse
        if (delta_vitesse < 0 and v + delta_vitesse > -self.vitesse_max):
            self.vitesse_gauche += delta_vitesse

    def appliquer_vitesse_droite(self, delta_vitesse):
        """
        Modifie la vitesse de la roue droite en ajoutant une variation de vitesse.
        
        :param delta_vitesse: Variation de la vitesse (positive ou négative)
        """
        v = self.vitesse_droite
        if (delta_vitesse > 0 and v + delta_vitesse < self.vitesse_max):
            self.vitesse_droite += delta_vitesse
        if (delta_vitesse < 0 and v + delta_vitesse > -self.vitesse_max):
            self.vitesse_droite += delta_vitesse

    def decelerer_robot(self):
        """
        Modifie la vitesse des deux roues en les ajustant pour qu'elle se rapproche du plus possible de la vitesse nulle.
        """
        
        if (self.vitesse_droite > 0 and self.vitesse_droite != 0):
            self.appliquer_vitesse_droite(-2)
        else:
            self.appliquer_vitesse_droite(2)

        if (self.vitesse_gauche > 0 and self.vitesse_gauche != 0):
            self.appliquer_vitesse_gauche(-2)
        else:
            self.appliquer_vitesse_gauche(2)
    

    def arreter_robot(self):
        """
        Modifie la vitesse de la roue droite et gauche en ajoutant la mettant à zero
        """
        self.vitesse_droite = 0
        self.vitesse_gauche = 0

    
    def cpadistance(self, environnement):
        """Retourne True et la distance si un obstacle est détecté devant le robot, False sinon."""
        
        angle = self.direction  # La direction du robot
        step = 1  # Distance entre chaque échantillon
        max_distance = 1000  # Distance maximale du capteur

        # Position initiale du capteur (centre du robot)
        x, y = self.x, self.y
        current_x, current_y = x, y

        # Parcourir la distance max
        for _ in range(int(max_distance / step)):
            # Avancer dans la direction du robot
            current_x += step * math.cos(angle)
            current_y += step * math.sin(angle)

            # Création d'un robot virtuel pour détecter la collision
            test_robot = Robot(current_x, current_y, direction=self.direction, taille_robot=self.taille_robot)

            # Vérification de collision avec les obstacles
            for obstacle in environnement.obstacles:
                collision=obstacle.detecter_collision(test_robot)
                if collision[0]:
                    distance = math.sqrt((current_x - x) ** 2 + (current_y - y) ** 2)
                    return True, distance

        return False, None  # Aucun obstacle détecté
