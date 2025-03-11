class RobotAdapter:
    # Constantes pour le contrôle du robot
    MOTOR_LEFT = "LEFT"
    MOTOR_RIGHT = "RIGHT"

    def __init__(self, robot):
        self.robot = robot

    def get_distance(self):
        """Retourne la distance à l'obstacle le plus proche."""
        obstacle_detecte, distance = self.robot.capteurdistance()
        return distance if obstacle_detecte else float("inf")
    
    def set_motor_dps(self, port, dps):
        """
        Fixe la vitesse d'un moteur en degrés par seconde (DPS).
        Conversion : DPS -> vitesse linéaire en mm/s -> application via les méthodes du robot.
        """
          # Conversion en mm/s

        if port == RobotAdapter.MOTOR_LEFT:
            self.robot.appliquer_vitesse_gauche(dps)
        elif port == RobotAdapter.MOTOR_RIGHT:
            self.robot.appliquer_vitesse_droite(dps)
    
