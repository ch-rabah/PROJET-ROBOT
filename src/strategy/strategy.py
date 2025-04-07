from adapter.adapter import RobotAdapter
class StrategyTourner(Strategy):
    def __init__(self, robot_adapter, angle_cible=0, vitesse=2):
        super().__init__(robot_adapter)
        self.angle_cible = angle_cible
        self.vitesse = vitesse

    def execute(self):
        """Faire tourner le robot jusqu'à atteindre l'angle cible."""
        if self.angle_cible > 0:
            self.robot_adapter.set_speed_left(self.vitesse)
            self.robot_adapter.set_speed_right(-self.vitesse)
        else:
            self.robot_adapter.set_speed_left(-self.vitesse)
            self.robot_adapter.set_speed_right(self.vitesse) 

        # Vérifier si l'angle cible est atteint
        if abs(self.robot_adapter.calculer_angle_parcouru()) >= abs(self.angle_cible):
            print(f"Angle cible atteint ({self.robot_adapter.calculer_angle_parcouru():.2f}°)")
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)

    def est_terminee(self):
        """Retourne True si l'angle cible est atteint."""
        return abs(self.robot_adapter.calculer_angle_parcouru()) >= abs(self.angle_cible)
class StrategySequentielle(Strategy):
    def __init__(self, robot_adapter, strategies):
        """
        :param strategies: Liste de stratégies à exécuter dans l'ordre
        """
        super().__init__(robot_adapter)
        self.strategies = strategies
        self.current_strategy_index = 0

    def execute(self):
        """Exécuter la stratégie actuelle et passer à la suivante quand elle est terminée."""
        if self.current_strategy_index >= len(self.strategies):
            return  # Toutes les stratégies sont terminées

        # Récupérer la stratégie actuelle à exécuter
        strategy_class, param = self.strategies[self.current_strategy_index]
        current_strategy = strategy_class(self.robot_adapter, *param)
        
        # Exécuter la stratégie actuelle
        current_strategy.execute()

        # Vérifier si elle est terminée
        if current_strategy.est_terminee():
            self.current_strategy_index += 1  # Passer à la suivante
class StrategieBleu(Strategy):
    def execute(self):
        self.set_dessine(True)  
        self.set_couleur("blue") 

    def est_terminee(self):
        return True 

class StrategieRouge(Strategy):
    def execute(self):
        self.set_dessine(True)  
        self.set_couleur("red")  

    def est_terminee(self):
        return True  

class StrategieInvisible(Strategy):
    def execute(self):
        self.set_dessine(False)  
        self.set_couleur("")  

    def est_terminee(self):
        return True

