from FWSFR.RobotReel.Robot2I013 import Robot2IN013
from FWSFR.algo_detection.algo import generer_masque_balise, position_balise_dans_image
import cv2
from math import *
import time


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

    def calculer_distance_parcourue(self):
        pass

    def calculer_angle_parcouru(self):
        pass

    def reset(self):
        self.angle_parcouru = 0
        self.distance_parcourue = 0
        # Ne pas toucher aux autres variables ici

class RobotAdapterSimulation(RobotAdapter):
    def __init__(self, robot, simulation=None):
        super().__init__()
        self.robot = robot  
        self.simulation = simulation
        self.previous_time = time.time()

    def set_speed_left(self, dps):
        self.robot.appliquer_vitesse_gauche(dps)

    def set_speed_right(self, dps):
        self.robot.appliquer_vitesse_droite(dps)

    def calculer_distance_parcourue(self):
        dt = self.get_dt()
        vitesse_moyenne = (self.robot.vitesse_gauche + self.robot.vitesse_droite) / 2
        distance = vitesse_moyenne * dt
        self.distance_parcourue += distance
        return self.distance_parcourue

    def calculer_angle_parcouru(self):
        dt = self.get_dt()
        delta_vitesse = self.robot.vitesse_droite - self.robot.vitesse_gauche
        angle = (delta_vitesse / self.robot.distance_roues) * dt  
        self.angle_parcouru += angle
        self.angle_parcouru = round(self.angle_parcouru, 4)
        return self.angle_parcouru * (180 / pi)

    def get_distance(self):
        obstacle_detecte, distance = self.robot.capteurdistance()
        return distance if obstacle_detecte else float("inf")

    def get_dt(self):
        current_time = time.time()
        dt = current_time - self.previous_time
        self.previous_time = current_time
        return dt

    def get_image(self):
        chemin = self.simulation.render()  # capture et sauvegarde un screenshot
        image_bgr = cv2.imread(chemin)     # lit l'image (par défaut en BGR)
        
        if image_bgr is None:
            print(f"[ERREUR] Impossible de lire l'image depuis : {chemin}")
            return None
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)  # conversion en RGB

        return image_rgb


class RobotAdapterReel(RobotAdapter):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.pos_initiale = self.robot.get_motor_position()  # Initialisation de la position des moteurs

    def set_speed_left(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps)

    def set_speed_right(self, dps):
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps)

    def calculer_distance_parcourue(self):
        l_pos_actuelle, r_pos_actuelle = self.robot.get_motor_position()

        distance_gauche = (l_pos_actuelle - self.pos_initiale[0]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)
        distance_droite = (r_pos_actuelle - self.pos_initiale[1]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)

        distance_moyenne = (distance_gauche + distance_droite) / 2
        self.distance_parcourue += distance_moyenne

        self.pos_initiale = (l_pos_actuelle, r_pos_actuelle)  # Mettre à jour la position initiale après chaque calcul
        return self.distance_parcourue

    def calculer_angle_parcouru(self):
        l_pos_actuelle, r_pos_actuelle = self.robot.get_motor_position()

        distance_gauche = (l_pos_actuelle - self.pos_initiale[0]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)
        distance_droite = (r_pos_actuelle - self.pos_initiale[1]) * (self.robot.WHEEL_DIAMETER * 3.14159 / 360)

        angle = (distance_droite - distance_gauche) / self.robot.WHEEL_BASE_WIDTH  
        self.angle_parcouru += angle
        self.angle_parcouru = round(self.angle_parcouru, 4)

        self.pos_initiale = (l_pos_actuelle, r_pos_actuelle)  # Mettre à jour la position initiale après chaque calcul
        return self.angle_parcouru * (180 / pi)

    def get_distance(self):
        return self.robot.get_distance()
    
    def get_image(self):
        return self.robot.get_image()

    def reset(self):
        super().reset()
        self.pos_initiale = self.robot.get_motor_position()  # Réinitialisation spécifique au robot réel
