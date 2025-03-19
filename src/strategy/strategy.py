from adapter.adapter import RobotAdapter

class Strategy:
    def __init__(self, robot_adapter):
        self.robot_adapter = robot_adapter

    def execute(self, dt):
        """Méthode à implémenter pour exécuter la stratégie."""
        pass

    def __call__(self):
        pass

    def est_terminee():
        pass

class StrategyAvancer(Strategy):
    def __init__(self, robot_adapter):
        super().__init__(robot_adapter)

    def execute(self, dt):
        self.robot_adapter.set_speed_left(self.vitesse)
        self.robot_adapter.set_speed_right(self.vitesse)

        self.distance_parcourue = self.robot_adapter.calculer_distance_parcourue(dt)

        # Vérifier si la distance cible est atteinte
        if self.distance_parcourue >= self.distance_cible:
            print(f"Distance cible atteinte ({self.distance_parcourue:.2f} mm)")
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)

    def __call__(self, distance_cible, vitesse=50):
        self.distance_cible = distance_cible
        self.vitesse = vitesse
        self.distance_parcourue = 0

    def est_terminee(self):
        if self.distance_parcourue >= self.distance_cible:  # Retourne True si l'objectif est atteint
            self.robot_adapter.reset()
            return True
        else:
            return False

class StrategyTourner(Strategy):
    def __init__(self, robot_adapter):
        super().__init__(robot_adapter)

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

    def __call__(self, angle_cible, vitesse=3):
        self.angle_cible = angle_cible
        self.vitesse = vitesse
        self.angle_parcouru = 0

    def est_terminee(self):
        if abs(self.angle_parcouru) >= abs(self.angle_cible):
            self.robot_adapter.reset()
            return True
        else:
            return False

class StrategyCarre(Strategy):
    def __init__(self, robot_adapter):
        super().__init__(robot_adapter)
        self.avancer = StrategyAvancer(robot_adapter)
        self.tourner = StrategyTourner(robot_adapter)
        self.current_strategy_index = 0

    def execute(self, dt):
        """Exécute les stratégies pour former un carré."""

        # Exécuter la stratégie actuelle
        if self.current_strategy_index < len(self.strategies):
            current_strategy, param = self.strategies[self.current_strategy_index]
            current_strategy(param)
            current_strategy.execute(dt)

            # Vérifier si la stratégie est terminée
            if current_strategy.est_terminee():
                self.current_strategy_index += 1

    def __call__(self, distance_cote):
        self.distance_cote = distance_cote
        self.current_step = 0
        self.strategies = [
            (self.avancer, self.distance_cote),
            (self.tourner, 90),
            (self.avancer, self.distance_cote),
            (self.tourner, 90),
            (self.avancer, self.distance_cote),
            (self.tourner, 90),
            (self.avancer, self.distance_cote),
            (self.tourner, 90),
        ]

    def est_terminee(self):
        if self.current_strategy_index >= len(self.strategies):
            return True
        else:
            return False
    
class StrategyConditionnelle(Strategy):
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

        # Vérifier si la stratégie actuelle est terminée avant d'en sélectionner une autre
        if self.current_strategy is None or self.current_strategy.est_terminee():
            self.current_strategy = None  # Réinitialisation de la stratégie terminée
            
            if self.condition_tourner:
                print("Condition tourner remplie, passage en mode tourner")
                self.current_strategy = StrategyTourner(self.robot_adapter)
                self.current_strategy(self.angle_degrees)
            
            elif self.condition_avancer:
                print("Condition avancer remplie, passage en mode avancer")
                self.current_strategy = StrategyAvancer(self.robot_adapter)
                self.current_strategy(self.distance_cible)
            
            elif self.condition_carre:
                print("Condition carré remplie, passage en mode carré")
                self.current_strategy = StrategyCarre(self.robot_adapter)
                self.current_strategy(self.distance_cote)
            
            else:
                print("Aucune condition remplie, arrêt de la stratégie")
                self.finished = True
                return True  # Arrêt définitif de la stratégie

        # Exécuter la stratégie actuelle si elle existe
        if self.current_strategy:
            self.current_strategy.execute(dt)

        return False  # La stratégie continue tant qu'il y a une action à exécuter

    def est_terminee(self):
        """Retourne True si la stratégie est terminée."""
        return self.finished or (self.current_strategy is not None and self.current_strategy.est_terminee())


class StrategySequentielle(Strategy):
    def __init__(self, robot_adapter, strategies):
        """
        Initialise une séquence de stratégies.
        
        :param robot_adapter: L'adaptateur du robot
        :param strategies: Liste de tuples (strategy, param)
        """
        super().__init__(robot_adapter)
        self.strategies = strategies
        self.current_strategy_index = 0
        self.current_strategy = None

    def execute(self, dt):
        """Exécute la stratégie actuelle et passe à la suivante quand elle est terminée."""
        if self.current_strategy_index >= len(self.strategies):
            return  # Toutes les stratégies sont terminées

        # Sélection de la stratégie actuelle si elle n'est pas déjà définie
        if self.current_strategy is None:
            strategy_class, param = self.strategies[self.current_strategy_index]
            self.current_strategy = strategy_class(self.robot_adapter)
            self.current_strategy(param)

        # Exécuter la stratégie actuelle
        self.current_strategy.execute(dt)

        # Vérifier si elle est terminée
        if self.current_strategy.est_terminee():
            self.current_strategy_index += 1
            self.current_strategy = None  # Réinitialiser pour passer à la suivante


        

    def est_terminee(self):
        """Retourne True si toutes les stratégies ont été exécutées."""
        return self.current_strategy_index >= len(self.strategies)
