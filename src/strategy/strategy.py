from adapter import RobotAdapter

class Strategy:
    def __init__(self, robot_adapter):
        self.robot_adapter = robot_adapter
        self.distance_parcourue = 0

    def __call__(self, dt):
        """Méthode à implémenter pour exécuter la stratégie."""
        pass

    def est_terminee():
        pass

class StrategyAvancer(Strategy):
    def __init__(self, robot_adapter, distance_cible, vitesse=50):
        super().__init__(robot_adapter)
        self.distance_cible = distance_cible
        self.vitesse = vitesse
        self.distance_parcourue = 0

    def execute(self, dt):
        self.robot_adapter.set_speed_left(self.vitesse)
        self.robot_adapter.set_speed_right(self.vitesse)

        self.distance_parcourue = self.robot_adapter.calculer_distance_parcourue(dt)

        # Vérifier si la distance cible est atteinte
        if self.distance_parcourue >= self.distance_cible:
            print(f"Distance cible atteinte ({self.distance_parcourue:.2f} mm)")
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)

    def est_terminee(self):
        if self.distance_parcourue >= self.distance_cible:  # Retourne True si l'objectif est atteint
            self.robot_adapter.reset()
            return True
        else:
            return False

class StrategyTourner(Strategy):
    def __init__(self, robot_adapter, angle_cible, vitesse=50):
        super().__init__(robot_adapter)
        self.angle_cible = angle_cible
        self.vitesse = vitesse
        self.angle_parcouru = 0

    def execute(self, dt):
        if self.angle_cible > 0:
            self.robot_adapter.set_speed_left(self.vitesse)
            self.robot_adapter.set_speed_right(-self.vitesse)
        else:
            self.robot_adapter.set_speed_left(-self.vitesse)
            self.robot_adapter.set_speed_right(self.vitesse)

        self.angle_parcouru = self.robot_adapter.calculer_angle_parcouru(dt)  # Conversion rad → degrés

        # Vérifier si l'angle cible est atteint
        if abs(self.angle_parcouru) >= abs(self.angle_cible):
            print(f"Angle cible atteint ({self.angle_parcouru:.2f}°)")
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)

    def est_terminee(self):
        if abs(self.angle_parcouru) >= abs(self.angle_cible):
            self.robot_adapter.reset()
            return True
        else:
            return False

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

    def execute(self, dt):
        """Exécute les stratégies pour former un carré."""
        if self.current_strategy_index < len(self.strategies):
            current_strategy = self.strategies[self.current_strategy_index]
            if current_strategy(dt):
                self.current_strategy_index += 1
                if self.current_strategy_index >= len(self.strategies):
                    return True  # Stratégie terminée
        return False  # Stratégie en cours
    
    def est_terminee():
        pass
    
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

    def execute(self, dt):
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

    def est_terminee(self):
        """Retourne True si la stratégie est terminée."""
        return self.finished #"""or (self.current_strategy is not None and self.current_strategy.is_finished())"""
