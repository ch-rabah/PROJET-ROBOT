from FWSFR.adapter.adapter import RobotAdapter
from FWSFR.algo_detection.algo import generer_masque_balise, position_balise_dans_image

class Strategy:
    def __init__(self, robot_adapter):
        self.robot_adapter = robot_adapter

    def execute(self):
        """Méthode à implémenter pour exécuter la stratégie."""
        pass

    def __call__(self):
        pass

    def est_terminee(self):
        pass

class StrategyAvancer(Strategy):
    def __init__(self, robot_adapter):
        super().__init__(robot_adapter)
        self.distance_cible = 0
        self.vitesse = 50

    def execute(self):
        self.robot_adapter.set_speed_left(self.vitesse)
        self.robot_adapter.set_speed_right(self.vitesse)     

        # Vérifier si la distance cible est atteinte
        if self.robot_adapter.calculer_distance_parcourue() >= self.distance_cible:
            print(f"Distance cible atteinte ({self.robot_adapter.calculer_distance_parcourue():.2f} mm)")
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)

    def __call__(self, distance_cible, vitesse=50):
        self.distance_cible = distance_cible
        self.vitesse = vitesse

    def est_terminee(self):
        if self.robot_adapter.calculer_distance_parcourue() >= self.distance_cible:  # Retourne True si l'objectif est atteint
            self.robot_adapter.reset()
            return True
        return False

class StrategyTourner(Strategy):
    def __init__(self, robot_adapter):
        super().__init__(robot_adapter)
        self.angle_cible = 0
        self.vitesse = 30

    def execute(self):
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

    def __call__(self, angle_cible, vitesse=30):
        self.angle_cible = angle_cible
        self.vitesse = vitesse

    def est_terminee(self):
        if abs(self.robot_adapter.calculer_angle_parcouru()) >= abs(self.angle_cible):
            self.robot_adapter.reset()
            return True
        return False

class StrategyConditionnelle(Strategy):
    def __init__(self, robot_adapter, strategy1, strategy2, condition_func):
        """
        - strategy1: tuple (StrategyInstance, param)
        - strategy2: tuple (StrategyInstance, param)
        - condition_func: fonction sans argument (ex: lambda: ...)
        """
        super().__init__(robot_adapter)
        strat1, self.param1 = strategy1
        strat2, self.param2 = strategy2

        # Si on passe la classe, on instancie, sinon on utilise l’instance déjà créée
        self.strategy1 = strat1(robot_adapter) if isinstance(strat1, type) else strat1
        self.strategy2 = strat2(robot_adapter) if isinstance(strat2, type) else strat2
        self.condition_func = condition_func
        self.current_strategy = None
        self.finished = False

    def __call__(self, param1=None, param2=None):
        """
        Remise à zéro complète de la stratégie + paramètres.
        Peut être appelée avec :
            - (param1, param2)
            - ((param1, param2),)
        """
        # Autorise le passage d’un tuple unique ((v1,v2),) ou de deux paramètres
        if isinstance(param1, tuple) and param2 is None:
            param1, param2 = param1
        if param1 is not None:
            self.param1 = param1
        if param2 is not None:
            self.param2 = param2
        self.current_strategy = None
        self.finished = False

    def execute(self):
        if self.finished:
            return True
        if self.current_strategy is None:
            if self.condition_func():
                self.current_strategy = self.strategy1
                self.param = self.param1
            else:
                self.current_strategy = self.strategy2
                self.param = self.param2
            self.current_strategy(self.param)
        self.current_strategy.execute()
        if self.current_strategy.est_terminee():
            self.finished = True
            return True
        return False

    def est_terminee(self):
        return self.finished


class StrategySequentielle(Strategy):
    def __init__(self, robot_adapter, strategies):
        """
        :param robot_adapter: L'adapter du robot (passé pour compatibilité)
        :param strategies: Liste de tuples (strategy_instance, param)
            - strategy_instance : instance déjà créée (pas la classe !)
            - param : peut être un seul argument, ou un tuple d'arguments à passer à __call__
        """
        super().__init__(robot_adapter)
        self.strategies = strategies
        self.current_strategy_index = 0
        self.current_strategy = None

    def execute(self):
        if self.current_strategy_index >= len(self.strategies):
            return  # Toutes les stratégies sont terminées

        if self.current_strategy is None:
            strategy_obj, param = self.strategies[self.current_strategy_index]
            # Appel __call__ de la stratégie avec unpack des paramètres si besoin
            if param is not None:
                # Si le param est un tuple, on déplie (ex: (40, 180) pour conditionnelle)
                if isinstance(param, tuple):
                    strategy_obj(*param)
                else:
                    strategy_obj(param)
            else:
                strategy_obj()
            self.current_strategy = strategy_obj

        self.current_strategy.execute()

        if self.current_strategy.est_terminee():
            self.current_strategy_index += 1
            self.current_strategy = None  # Passe à la suivante

    def est_terminee(self):
        return self.current_strategy_index >= len(self.strategies)



class StrategySuivreBalise(Strategy):
    def __init__(self, robot_adapter):
        super().__init__(robot_adapter)
        self.terminee = False

    def __call__(self):
        self.terminee = False

    def execute(self):
        if self.terminee:
            return

        image = self.robot_adapter.get_image()
        if image is None:
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)
            self.terminee = True
            return

        masque = generer_masque_balise(image)
        position = position_balise_dans_image(masque)

        if position is None:
            # Rien détecté : on arrête tout, stratégie finie
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)
            self.terminee = True
            print("Balise non détectée, arrêt de la stratégie.")
        else:
            # On suit la balise selon sa position dans l’image
            if position == "gauche":
                self.robot_adapter.set_speed_left(10)
                self.robot_adapter.set_speed_right(30)
            elif position == "droite":
                self.robot_adapter.set_speed_left(30)
                self.robot_adapter.set_speed_right(10)
            else:
                self.robot_adapter.set_speed_left(30)
                self.robot_adapter.set_speed_right(30)

    def est_terminee(self):
        return self.terminee
