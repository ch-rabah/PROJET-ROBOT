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
        self.robot = robot

    def set_speed_left(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps)

    def set_speed_right(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps)

    def calculer_distance_parcourue(self):
        pass

    def get_distance(self):
        return self.robot.get_distance()