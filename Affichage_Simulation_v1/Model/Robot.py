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

            # Vérification de collision avec les obstacles
            for obstacle in environnement.obstacles:
                collision=obstacle.detecter_collision((current_x,current_y))
                if collision:
                    distance = math.sqrt((current_x - x) ** 2 + (current_y - y) ** 2)
                    return True, distance

        return False, None  # Aucun obstacle détecté

    def points(self):
        """
        Retourne les trois sommets du triangle représentant le robot, avec un point qui se trouve entre chaque 2 sommets (cette fonctions sert a tester les collisions avec ces points)
        """
        p1 = (self.x + self.taille_robot * math.cos(self.direction - math.pi / 2),
              self.y + self.taille_robot * math.sin(self.direction - math.pi / 2))
        p2 = (self.x + self.taille_robot * math.cos(self.direction + math.pi / 2),
              self.y + self.taille_robot * math.sin(self.direction + math.pi / 2))
        p3 = (self.x + self.taille_robot * math.cos(self.direction + math.pi),
              self.y + self.taille_robot * math.sin(self.direction + math.pi))
        x1, y1=p1
        x2, y2=p2
        x3, y3=p3
        return [p1, p2, p3, (self.x,self.y),((x2+x3)/2,((y2+y3)/2)),((x1+x3)/2,((y1+y3)/2))]

    def suivre_carre(self, dt):
        """
        Fait suivre au robot une trajectoire en carré.
        Le robot avance, tourne à 90° et répète cela 4 fois.
        """
        if not hasattr(self, "etat_mouvement"):
            self.etat_mouvement = 0  # 0: Avancer, 1: Tourner
            self.etape = 0  # Numéro de l'étape dans le carré
            self.temps_restant = 2  # Temps pour avancer sur un côté (ajuster selon la vitesse)
        
        if self.etape >= 4:
            self.arreter_robot()
            return  # Carré terminé

        if self.etat_mouvement == 0:  # Avancer
            self.vitesse_gauche = self.vitesse_max / 2
            self.vitesse_droite = self.vitesse_max / 2
            self.temps_restant -= dt
            if self.temps_restant <= 0:
                self.etat_mouvement = 1
                self.temps_restant = 1  # Temps pour tourner

        elif self.etat_mouvement == 1:  # Tourner
            self.vitesse_gauche = -self.vitesse_max / 4
            self.vitesse_droite = self.vitesse_max / 4
            self.temps_restant -= dt
            if self.temps_restant <= 0:
                self.etape += 1
                self.etat_mouvement = 0
                self.temps_restant = 2  # Reprendre l'avance

            # Appliquer les vitesses aux roues
        self.avancer(dt)







