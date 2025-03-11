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
    
