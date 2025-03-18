#from robot2I013 import Robot2I013
from math import *

class RobotAdapter:
    def __init__(self):
        self.angle_parcouru = 0
        self.distance_parcourue = 0

    def set_speed_left(self, dps):
        pass

    def set_speed_right(self, dps):
        pass

    def get_distance(self):
        pass

    def calculer_distance_parcourue(self, dt):
        pass

    def calculer_angle_parcouru(self, dt):
        pass

    def reset(self):
        self.angle_parcouru = 0
        self.distance_parcourue = 0

class RobotAdapterSimulation(RobotAdapter):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot  # Pas de position initiale ici

    def set_speed_left(self, dps):
        self.robot.appliquer_vitesse_gauche(dps)

    def set_speed_right(self, dps):
        self.robot.appliquer_vitesse_droite(dps)

    def calculer_distance_parcourue(self, dt):
        """Simulation : calcul basé sur la vitesse moyenne et le temps écoulé."""
        vitesse_moyenne = (self.robot.vitesse_gauche + self.robot.vitesse_droite) / 2
        distance = vitesse_moyenne * dt
        self.distance_parcourue += distance
        return self.distance_parcourue

    def calculer_angle_parcouru(self, dt):
        """Simulation : calcul de l’angle basé sur la différence de vitesse."""
        delta_vitesse = self.robot.vitesse_droite - self.robot.vitesse_gauche
        angle = (delta_vitesse / self.robot.distance_roues) * dt  # En radians
        self.angle_parcouru += angle
        self.angle_parcouru = round(self.angle_parcouru, 4)
        return self.angle_parcouru * (180 / pi)

    def get_distance(self):
        """Retourne la distance à l'obstacle le plus proche."""
        obstacle_detecte, distance = self.robot.capteurdistance()
        return distance if obstacle_detecte else float("inf")
    
    def reset(self):
        super().reset()

class RobotAdapterReel(RobotAdapter):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.pos_initiale = self.robot.get_motor_position()  # Position initiale des roues

    def set_speed_left(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps)

    def set_speed_right(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps)

    def calculer_distance_parcourue(self, dt):
        """Calcul basé sur les encodeurs du robot réel."""
        l_pos_actuelle, r_pos_actuelle = self.robot.get_motor_position()

        distance_gauche = (l_pos_actuelle - self.pos_initiale[0]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)
        distance_droite = (r_pos_actuelle - self.pos_initiale[1]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)

        distance_moyenne = (distance_gauche + distance_droite) / 2
        self.distance_parcourue += distance_moyenne

        self.pos_initiale = (l_pos_actuelle, r_pos_actuelle)  
        return self.distance_parcourue

    def calculer_angle_parcouru(self, dt):
        """Calcul de l’angle parcouru basé sur les encodeurs."""
        l_pos_actuelle, r_pos_actuelle = self.robot.get_motor_position()

        distance_gauche = (l_pos_actuelle - self.pos_initiale[0]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)
        distance_droite = (r_pos_actuelle - self.pos_initiale[1]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)

        angle = (distance_droite - distance_gauche) / self.robot.WHEEL_BASE_WIDTH  # En radians
        self.angle_parcouru += angle
        self.angle_parcouru = round(self.angle_parcouru, 4)

        self.pos_initiale = (l_pos_actuelle, r_pos_actuelle)  # Mise à jour de la position initiale
        return self.angle_parcouru * (180 / pi)

    def get_distance(self):
        return self.robot.get_distance()