#from robot2I013 import Robot2I013

class RobotAdapter:
    def set_speed_left(self, dps):
        pass

    def set_speed_right(self, dps):
        pass

    def get_distance(self):
        pass

    def calculer_distance_parcourue(self, dt):
        pass

class RobotAdapterSimulation(RobotAdapter):
    def __init__(self, robot):
        self.robot = robot

    def set_speed_left(self, dps):
        # Implémentation pour la simulation
        self.robot.appliquer_vitesse_gauche(dps)

    def set_speed_right(self, dps):
        # Implémentation pour la simulation
        self.robot.appliquer_vitesse_droite(dps)

    def calculer_distance_parcourue(self, dt):
        # Implémentation pour la simulation
        vitesse_moyenne = (self.robot.vitesse_gauche + self.robot.vitesse_droite) / 2
        distance = vitesse_moyenne * dt
        return distance
    
    def get_distance(self):
        """Retourne la distance à l'obstacle le plus proche."""
        obstacle_detecte, distance = self.robot.capteurdistance()
        return distance if obstacle_detecte else float("inf")

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