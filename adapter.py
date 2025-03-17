class RobotAdapter:
    def set_speed_left(self, dps):
        pass

    def set_speed_right(self, dps):
        pass

    def calculer_distance_parcourue(self, vitesse_gauche, vitesse_droite, dt):
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

    def calculer_distance_parcourue(self, vitesse_gauche, vitesse_droite, dt):
        # Implémentation pour la simulation
        vitesse_moyenne = (vitesse_gauche + vitesse_droite) / 2
        distance = vitesse_moyenne * dt
        return distance

class RobotAdapterReel(RobotAdapter):
    MOTOR_LEFT = "LEFT"
    MOTOR_RIGHT = "RIGHT"

    def __init__(self, robot):
        self.robot = robot

    def set_speed_left(self, dps):
        set_motor_dps(RobotAdapterReel.MOTOR_LEFT, dps)

    def set_speed_right(self, dps):
        self.set_motor_dps(RobotAdapterReel.MOTOR_RIGHT, dps)

    def calculer_distance_parcourue(self):
        pass