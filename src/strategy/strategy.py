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

class StrategyTourner(Strategy):
    def __init__(self, robot_adapter, angle_degrees):
        super().__init__(robot_adapter)
        self.angle_degrees = angle_degrees
        self.angle_parcouru = 0
        self.base_robot = 30  # Distance entre les roues du robot en mm (à ajuster selon votre robot)
        self.vitesse = 20 if angle_degrees > 0 else -20

    def __call__(self, dt):
        """Tourne jusqu'à atteindre l'angle cible."""

        # Appliquer la vitesse au robot
        self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_LEFT, self.vitesse)
        self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_RIGHT, -self.vitesse)

        # Calculer la vitesse angulaire (en degrés par seconde)
        vitesse_angulaire = (self.vitesse + self.vitesse) / self.base_robot * (180 / 3.14159)

        # Calculer l'angle parcouru
        self.angle_parcouru += vitesse_angulaire * dt

        # Vérifier si l'angle cible est atteint
        if abs(self.angle_parcouru) >= abs(self.angle_degrees):
            print(f"Angle cible atteint ({self.angle_parcouru}°)")
            self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_LEFT, 0)
            self.robot_adapter.set_motor_dps(RobotAdapter.MOTOR_RIGHT, 0)
            return True  # Stratégie terminée
        return False  # Stratégie en cours

class StrategyCarre(Strategy):
    def __init__(self, robot_adapter, distance_cote):
        super().__init__(robot_adapter)
        self.distance_cote = distance_cote
        self.strategies = [
            StrategyAvancer(robot_adapter, distance_cote),
            StrategyTourner(robot_adapter, 90),
            StrategyAvancer(robot_adapter, distance_cote),
            StrategyTourner(robot_adapter, 90),
            StrategyAvancer(robot_adapter, distance_cote),
            StrategyTourner(robot_adapter, 90),
            StrategyAvancer(robot_adapter, distance_cote),
            StrategyTourner(robot_adapter, 90)
        ]
        self.current_strategy_index = 0

    def __call__(self, dt):
        """Exécute les stratégies pour former un carré."""
        if self.current_strategy_index < len(self.strategies):
            current_strategy = self.strategies[self.current_strategy_index]
            if current_strategy(dt):
                self.current_strategy_index += 1
                if self.current_strategy_index >= len(self.strategies):
                    return True  # Stratégie terminée
        return False  # Stratégie en cours
    
class StrategyConditionnel(Strategy):
    def __init__(self, robot_adapter, distance_cible, angle_degrees, distance_cote, condition_tourner, condition_avancer, condition_carre):
        super().__init__(robot_adapter)
        self.distance_cible = distance_cible
        self.angle_degrees = angle_degrees
        self.distance_cote = distance_cote
        self.condition_tourner = condition_tourner
        self.condition_avancer = condition_avancer
        self.condition_carre = condition_carre
        self.current_strategy = None
        self.finished = False

    def __call__(self, dt):
        """Exécute la stratégie en fonction des conditions."""
        if self.finished:
            return True  # Stratégie déjà terminée

        if self.current_strategy is None: #"""or self.current_strategy.is_finished()""":
            if self.condition_tourner():
                print("Condition tourner remplie, passage en mode tourner")
                self.current_strategy = StrategyTourner(self.robot_adapter, self.angle_degrees)
            elif self.condition_avancer():
                print("Condition avancer remplie, passage en mode avancer")
                self.current_strategy = StrategyAvancer(self.robot_adapter, self.distance_cible)
            elif self.condition_carre():
                print("Condition carre remplie, passage en mode carré")
                self.current_strategy = StrategyCarre(self.robot_adapter, self.distance_cote)
            else:
                print("Aucune condition remplie, arrêt de la stratégie")
                self.finished = True
                return True  # Arrêt définitif de la stratégie

        return False  # La stratégie continue tant qu'il y a une action à exécuter

    def is_finished(self):
        """Retourne True si la stratégie est terminée."""
        return self.finished #"""or (self.current_strategy is not None and self.current_strategy.is_finished())"""
