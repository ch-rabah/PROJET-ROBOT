import math


class Robot:
    def __init__(self, x, y, direction=0, vitesse_gauche=0, vitesse_droite=0, distance_roues=30,taille_robot=20):
        """
        Initialise un robot différentiel avec position, direction, et vitesses de roues.
        
        :param x: Position initiale en x
        :param y: Position initiale en y
        :param direction: Direction initiale du robot (en radians)
        :param vitesse_gauche: Vitesse initiale de la roue gauche (en unités par seconde)
        :param vitesse_droite: Vitesse initiale de la roue droite (en unités par seconde)
        :param distance_roues: Distance entre les roues (en unités)
        :param taille_robot: Taille du robot (utilisé pour les collisions)

        """
        self.x = x
        self.y = y
        self.direction = direction  # Direction en radians
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.distance_roues = distance_roues
        self.taille_robot = taille_robot
        
    def avancer(self, dt):
        """
        Met à jour la position du robot en fonction de la vitesse et du temps écoulé.
        
        :param dt: Intervalle de temps (en secondes)
        """
        # Mise à jour des positions P2.x et P2.y avec la vitesse actuelle
        self.x += self.vx * dt
        self.y += self.vy * dt

    def rotation(self, angle_degrees):
        """
        Fait tourner le robot d'un certain angle en degrés, en modifiant sa direction.
        
        :param angle_degrees: Angle de rotation en degrés
        """
        angle_radians = math.radians(angle_degrees)
        self.direction += angle_radians

        # Mettre à jour la direction de la vitesse en fonction du nouvel angle
        new_vx = self.vx * math.cos(angle_radians) - self.vy * math.sin(angle_radians)
        new_vy = self.vx * math.sin(angle_radians) + self.vy * math.cos(angle_radians)
        self.vx, self.vy = new_vx, new_vy
    
    def tourner(robot, angle_total, duree, dt, angle_cumule):
        """
        Fait tourner le robot progressivement sans dépasser l'angle cible.
        """
        angle_par_dt = (angle_total / duree) * dt

        # Limiter l'angle restant à tourner pour ne pas dépasser l'angle total
        angle_restant = angle_total - angle_cumule
        angle_a_tourner = min(angle_par_dt, angle_restant)

        robot.rotation(angle_a_tourner)

        angle_cumule += angle_a_tourner
        rotation_terminee = angle_cumule >= angle_total
        return rotation_terminee, angle_cumule



    def mettre_a_jour_vitesse(self, dt):
        """
        Met à jour la vitesse du robot en fonction de l'accélération et du temps écoulé.
        
        :param dt: Intervalle de temps (en secondes)
        """
        self.vx += self.ax * dt
        self.vy += self.ay * dt



