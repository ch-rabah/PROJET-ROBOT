from FWSFR.algo_detection.algo import generer_masque_balise, position_balise_dans_image
import cv2
from math import *
import time


class RobotAdapter:
    """ 
    Classe abstraite servant d’interface entre le robot (réel ou simulé) et les stratégies.
    Définit les méthodes communes à toute implémentation de robot, réelle ou simulée.
    """
    def __init__(self):
        """
        Initialise les variables de suivi pour la distance et l’angle parcourus.
        """
        self.angle_parcouru = 0
        self.distance_parcourue = 0

    def set_speed_left(self, dps):
        """
        Définit la vitesse de la roue gauche du robot en degrés par seconde (dps).
        À implémenter dans les classes dérivées.
        
        :param dps: Vitesse à appliquer à la roue gauche (en degrés par seconde)
        """
        pass

    def set_speed_right(self, dps):
        """
        Définit la vitesse de la roue droite du robot en degrés par seconde (dps).
        À implémenter dans les classes dérivées.
        
        :param dps: Vitesse à appliquer à la roue droite (en degrés par seconde)
        """
        pass

    def get_distance(self):
        """
        Récupère la distance jusqu’à l’obstacle détecté devant le robot.
        À implémenter dans les classes dérivées.
        
        :return: Distance en unités appropriées (mm/cm/m), ou float("inf") si aucun obstacle détecté
        """
        pass

    def calculer_distance_parcourue(self):
        """
        Calcule et met à jour la distance totale parcourue par le robot.
        À implémenter dans les classes dérivées.
        
        :return: Distance totale parcourue depuis le dernier reset.
        """
        pass

    def calculer_angle_parcouru(self):
        """
        Calcule et met à jour l’angle total parcouru (en degrés) par le robot.
        À implémenter dans les classes dérivées.
        
        :return: Angle total parcouru depuis le dernier reset.
        """
        pass

    def get_image(self):
        """
        Capture et retourne une image vue par le robot (caméra embarquée ou vue simulée).
        À implémenter dans les classes dérivées.
        
        :return: Image (généralement sous forme de tableau numpy ou format adapté à l’analyse d’image).
        """
        pass

    def reset(self):
        """
        Réinitialise la distance et l’angle parcourus à zéro.
        À utiliser lors d’un changement de stratégie ou de contexte.
        """
        self.angle_parcouru = 0
        self.distance_parcourue = 0
        # Ne pas toucher aux autres variables ici

class RobotAdapterSimulation(RobotAdapter):
    def __init__(self, robot, simulation=None):
        """
        Initialise l’adaptateur pour un robot simulé.
        :param robot: Instance du robot simulé à adapter
        :param simulation: Instance de la simulation 
        """
        super().__init__()
        self.robot = robot  
        self.simulation = simulation
        self.previous_time = time.time()

    def set_speed_left(self, dps):
        """ Définit la vitesse de la roue gauche du robot simulé.
        :param dps: Vitesse à appliquer à la roue gauche (en degrés par seconde)
        """
        self.robot.appliquer_vitesse_gauche(dps)

    def set_speed_right(self, dps):
        """ Définit la vitesse de la roue droite du robot simulé.
        :param dps: Vitesse à appliquer à la roue droite (en degrés par seconde)
        """
        self.robot.appliquer_vitesse_droite(dps)

    def calculer_distance_parcourue(self):
        """
        Calcule et met à jour la distance totale parcourue par le robot simulé.
        :return: Distance totale parcourue depuis le dernier reset.
        """
        dt = self.get_dt()
        vitesse_moyenne = (self.robot.vitesse_gauche + self.robot.vitesse_droite) / 2
        distance = vitesse_moyenne * dt
        self.distance_parcourue += distance
        return self.distance_parcourue

    def calculer_angle_parcouru(self):
        """
        Calcule et met à jour l’angle total parcouru (en degrés) par le robot simulé.
        :return: Angle total parcouru depuis le dernier reset.
        """
        dt = self.get_dt()
        delta_vitesse = self.robot.vitesse_droite - self.robot.vitesse_gauche
        angle = (delta_vitesse / self.robot.distance_roues) * dt  
        self.angle_parcouru += angle
        self.angle_parcouru = round(self.angle_parcouru, 4)
        return self.angle_parcouru * (180 / pi)

    def get_distance(self):
        """
        Récupère la distance jusqu’à l’obstacle détecté devant le robot simulé.
        :return: Distance en unités appropriées (mm/cm/m), ou float("inf") si aucun obstacle détecté
        """
        obstacle_detecte, distance = self.robot.capteurdistance()
        return distance if obstacle_detecte else float("inf")

    def get_dt(self):
        """ 
        Calcule le temps écoulé depuis la dernière mise à jour.
        :return: Temps écoulé en secondes
        """
        current_time = time.time()
        dt = current_time - self.previous_time
        self.previous_time = current_time
        return dt

    def get_image(self):
        """
        Capture et retourne une image vue par le robot simulé.
        :return: Image (généralement sous forme de tableau numpy ou format adapté à l’analyse d’image RGB).
        """
        chemin = self.simulation.render()  # capture et sauvegarde un screenshot
        image_bgr = cv2.imread(chemin)     # lit l'image (par défaut en BGR)
        
        if image_bgr is None:
            print(f"[ERREUR] Impossible de lire l'image depuis : {chemin}")
            return None
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)  # conversion en RGB

        return image_rgb


class RobotAdapterReel(RobotAdapter):
    def __init__(self,robot):
        """
        Initialise l’adaptateur pour un robot réel.
        :param robot: Instance du robot réel à adapter
        """
        super().__init__()
        self.robot = robot
        self.pos_initiale = self.robot.get_motor_position()# Initialisation de la position des moteurs
        self.robot.start_recording()  

    def set_speed_left(self, dps):
        """ 
        Définit la vitesse de la roue gauche du robot réel en appelant la méthode appropriée de l'API du robot.
        :param dps: Vitesse à appliquer à la roue gauche (en degrés par seconde)
        """
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps)

    def set_speed_right(self, dps):
        """ 
        Définit la vitesse de la roue droite du robot réel en appelant la méthode appropriée de l'API du robot.
        :param dps: Vitesse à appliquer à la roue droite (en degrés par seconde)
        """
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps)

    def calculer_distance_parcourue(self):
        """
        Calcule et met à jour la distance totale parcourue par le robot réel.
        :return: Distance totale parcourue depuis le dernier reset.
        """
        l_pos_actuelle, r_pos_actuelle = self.robot.get_motor_position()

        distance_gauche = (l_pos_actuelle - self.pos_initiale[0]) * (self.robot.WHEEL_DIAMETER * pi / 360)
        distance_droite = (r_pos_actuelle - self.pos_initiale[1]) * (self.robot.WHEEL_DIAMETER * pi / 360)

        distance_moyenne = (distance_gauche + distance_droite) / 2
        self.distance_parcourue += distance_moyenne

        self.pos_initiale = (l_pos_actuelle, r_pos_actuelle)  # Mettre à jour la position initiale après chaque calcul
        return self.distance_parcourue

    def calculer_angle_parcouru(self):
        """ 
        Calcule et met à jour l’angle total parcouru (en degrés) par le robot réel.
        :return: Angle total parcouru depuis le dernier reset.
        """
        l_pos_actuelle, r_pos_actuelle = self.robot.get_motor_position()

        distance_gauche = (l_pos_actuelle - self.pos_initiale[0]) * (self.robot.WHEEL_DIAMETER * pi / 360)
        distance_droite = (r_pos_actuelle - self.pos_initiale[1]) * (self.robot.WHEEL_DIAMETER * pi / 360)

        angle = (distance_droite - distance_gauche) / self.robot.WHEEL_BASE_WIDTH  
        self.angle_parcouru += angle
        self.angle_parcouru = round(self.angle_parcouru, 4)

        self.pos_initiale = (l_pos_actuelle, r_pos_actuelle)  # Mettre à jour la position initiale après chaque calcul
        return self.angle_parcouru * (180 / pi)

    def get_distance(self):
        """ 
        Récupère la distance jusqu’à l’obstacle détecté devant le robot réel en appelant la méthode appropriée de l'API du robot.
        :return: Distance en unités, ou float("inf") si aucun obstacle détecté
        """
        return self.robot.get_distance()
    
    def get_image(self):
        """
        Capture et retourne une image vue par le robot réel en appelant la méthode appropriée de l'API du robot.
        :return: Image (sous forme de tableau numpy ou format adapté à l’analyse d’image RGB).
        """
        return self.robot.get_image()

    def reset(self):
        """ Réinitialise la distance et l’angle parcourus à zéro, ainsi que la position initiale des moteurs."""
        super().reset()
        self.pos_initiale = self.robot.get_motor_position()  # Réinitialisation spécifique au robot réel
