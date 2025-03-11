from adapter import RobotAdapter

class Strategy:
    def __init__(self, robot_adapter):
        self.robot_adapter = robot_adapter
        self.distance_parcourue = 0

    def __call__(self, dt):
        """Méthode à implémenter pour exécuter la stratégie."""
        pass

class StrategyAvancer(Strategy):
    def __init__(self, robot, distance_cible):
        super().__init__(robot)
        self.distance_cible = distance_cible

    def __call__(self, dt):
        """Avance jusqu'à atteindre la distance cible."""
        self.vitesse_gauche = 20
        self.vitesse_droite = 20

        # Calculer la distance parcourue
        self.distance_parcourue += self.robot_adapter.calculer_distance_parcourue(self.vitesse_gauche, self.vitesse_droite, dt)

        # Appliquer la vitesse au robot
        self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_LEFT, self.vitesse_gauche)
        self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_RIGHT, self.vitesse_droite)

        # Vérifier si la distance cible est atteinte
        if self.distance_parcourue >= self.distance_cible:
            print(f"Distance cible atteinte ({self.distance_parcourue} mm)")
            self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_LEFT, 0)
            self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_RIGHT, 0)
            return True  # Stratégie terminée
        return False  # Stratégie en cours