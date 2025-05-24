from FWSFR.adapter.adapter import RobotAdapter

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
        self.vitesse = 30

    def execute(self):
        self.robot_adapter.set_speed_left(self.vitesse)
        self.robot_adapter.set_speed_right(self.vitesse)

        

        # Vérifier si la distance cible est atteinte
        if self.robot_adapter.calculer_distance_parcourue() >= self.distance_cible:
            print(f"Distance cible atteinte ({self.robot_adapter.calculer_distance_parcourue():.2f} mm)")
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)

    def __call__(self, distance_cible, vitesse=30):
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
        self.vitesse = 2

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

    def __call__(self, angle_cible, vitesse=2):
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
        Initialise la stratégie conditionnelle avec deux stratégies et une fonction de condition.

        :param robot_adapter: L'adaptateur du robot
        :param strategy1: Première stratégie sous forme d'un Tuple (Strategy, param) si la condition est vraie
        :param strategy2: Deuxième stratégie sous forme d'un Tuple (Strategy, param) si la condition est fausse
        :param condition_func: Fonction qui retourne True ou False pour déterminer la stratégie à exécuter
        """
        super().__init__(robot_adapter)
        strat1, self.param1 = strategy1
        strat2, self.param2 = strategy2
        self.strategy1 = strat1(robot_adapter)
        self.strategy2 = strat2(robot_adapter)
        self.condition_func = condition_func  # Maintenant, c'est une fonction, pas un booléen
        self.current_strategy = None
        self.finished = False

    def execute(self):
        """Exécute la stratégie en fonction du résultat de la fonction condition."""
        if self.finished:
            return True  # Stratégie déjà terminée

        # Vérifier la condition via la fonction conditionnelle
        if self.current_strategy is None:
            if self.condition_func():  # Appel de la fonction conditionnelle
                print("Condition remplie, exécution de la première stratégie")
                self.current_strategy = self.strategy1
                self.param = self.param1
            else:
                print("Condition non remplie, exécution de la deuxième stratégie")
                self.current_strategy = self.strategy2
                self.param = self.param2
            
            print(f"Stratégie choisie : {self.current_strategy}")  # Affichage de la stratégie choisie
            self.current_strategy(self.param)

        # Exécuter la stratégie actuelle
        self.current_strategy.execute()

        # Vérifier si la stratégie est terminée
        if self.current_strategy.est_terminee():
            self.finished = True
            print(f"Stratégie terminée : {self.current_strategy}")
            return True

        return False  # La stratégie continue

    def est_terminee(self):
        """Retourne True si la stratégie est terminée."""
        return self.finished


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

    def execute(self):
        """Exécute la stratégie actuelle et passe à la suivante quand elle est terminée."""
        if self.current_strategy_index >= len(self.strategies):
            return  # Toutes les stratégies sont terminées

        # Sélection de la stratégie actuelle si elle n'est pas déjà définie
        if self.current_strategy is None:
            strategy_class, param = self.strategies[self.current_strategy_index]
            self.current_strategy = strategy_class(self.robot_adapter)
            self.current_strategy(param)

        # Exécuter la stratégie actuelle
        self.current_strategy.execute()

        # Vérifier si elle est terminée
        if self.current_strategy.est_terminee():
            self.current_strategy_index += 1
            self.current_strategy = None  # Réinitialiser pour passer à la suivante

    def est_terminee(self):
        """Retourne True si toutes les stratégies ont été exécutées."""
        return self.current_strategy_index >= len(self.strategies)



class StrategySuivreBalise(Strategy):
    def __init__(self, robot_adapter):
        super().__init__(robot_adapter)
        self.etat = "cherche"         # "cherche" ou "suit"
        self.terminee = False

    def execute(self):
        if self.terminee:
            return

        if self.etat == "cherche":
            position = self.robot_adapter.analyser_position_balise()

            if position is None:
                self.robot_adapter.set_speed_left(15)
                self.robot_adapter.set_speed_right(-15)
                angle = self.robot_adapter.calculer_angle_parcouru()

                if abs(angle) >= 360:
                    print("Tour complet sans balise. Fin de stratégie.")
                    self.robot_adapter.set_speed_left(0)
                    self.robot_adapter.set_speed_right(0)
                    self.terminee = True
            else:
                print(f"Balise détectée à : {position}")
                self.etat = "suit"
                self.robot_adapter.reset()  # reset angle/distance pour la phase suivante

        elif self.etat == "suit":
            position = self.robot_adapter.analyser_position_balise()

            if position is None:
                print("Balise perdue. Retour à la recherche.")
                self.etat = "cherche"
                self.robot_adapter.reset()
                return

            if position == "gauche":
                self.robot_adapter.set_speed_left(15)
                self.robot_adapter.set_speed_right(30)
            elif position == "droite":
                self.robot_adapter.set_speed_left(30)
                self.robot_adapter.set_speed_right(15)
            else:
                self.robot_adapter.set_speed_left(30)
                self.robot_adapter.set_speed_right(30)

    def est_terminee(self):
        return self.terminee
