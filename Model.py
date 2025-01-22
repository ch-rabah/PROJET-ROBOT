import math
import numpy as np


class Robot:
    def __init__(self, x, y, vx, vy, ax=0, ay=0, direction=0):
        """
        Initialise un robot avec la position, la vitesse, l'accélération et la direction initiale.
        
        :param x: Position initiale en x
        :param y: Position initiale en y
        :param vx: Vitesse initiale sur l'axe x
        :param vy: Vitesse initiale sur l'axe y
        :param ax: Accélération initiale sur l'axe x (optionnel)
        :param ay: Accélération initiale sur l'axe y (optionnel)
        :param direction: Direction initiale du robot (en radians, 0 par défaut)
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.direction = direction  # Direction du robot (en radians)

    def avancer(self, dt):
        """
        Met à jour la position du robot en fonction de la vitesse et du temps écoulé.
        
        :param dt: Intervalle de temps (en secondes)
        """
        # Mise à jour des positions P2.x et P2.y avec la vitesse actuelle
        self.x += self.vx * dt
        self.y += self.vy * dt

    def tourner(self, angle_degrees):
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


    def mettre_a_jour_vitesse(self, dt):
        """
        Met à jour la vitesse du robot en fonction de l'accélération et du temps écoulé.
        
        :param dt: Intervalle de temps (en secondes)
        """
        self.vx += self.ax * dt
        self.vy += self.ay * dt

    def appliquer_acceleration(self, ax, ay):
        """
        Applique une nouvelle accélération au robot.
        
        :param ax: Nouvelle accélération sur l'axe x
        :param ay: Nouvelle accélération sur l'axe y
        """
        self.ax = ax
        self.ay = ay

    def obtenir_position(self):
        """
        Retourne la position actuelle du robot.
        """
        return (self.x, self.y)

    def obtenir_vitesse(self):
        """
        Retourne la vitesse actuelle du robot.
        """
        return (self.vx, self.vy)

    def obtenir_direction(self):
        """
        Retourne la direction actuelle du robot (en radians).
        """
        return self.direction
