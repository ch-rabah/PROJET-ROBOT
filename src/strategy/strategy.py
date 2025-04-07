from adapter.adapter import RobotAdapter

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
    def __init__(self, robot_adapter, strategy1, strategy2, condition):
        """
        Initialise la stratégie conditionnelle avec deux stratégies et une condition.
        
        :param robot_adapter: L'adaptateur du robot
        :param strategy1: Première stratégie sous forme d'un Tuple (Strategie, parametre) (si condition est vraie)
        :param strategy2: Deuxième stratégie sous forme d'un Tuple (Strategie, parametre) (si condition est fausse)
        :param condition: un booléen (expression)
        """
        super().__init__(robot_adapter)
        strat1, self.param1 = strategy1
        strat2, self.param2 = strategy2
        self.strategy1 = strat1(robot_adapter)
        self.strategy2 = strat2(robot_adapter)
        self.condition = condition
        self.current_strategy = None
        self.finished = False

    def execute(self):
        """Exécute la stratégie en fonction de la condition."""
        if self.finished:
            return True  # Stratégie déjà terminée

        # Déterminer la stratégie à exécuter
        if self.current_strategy is None:
            if self.condition:
                print("Condition remplie, exécution de la première stratégie")
                self.current_strategy = self.strategy1
                self.param = self.param1
            else:
                print("Condition non remplie, exécution de la deuxième stratégie")
                self.current_strategy = self.strategy2
                self.param = self.param2
            self.current_strategy(self.param)

        # Exécuter la stratégie actuelle
        self.current_strategy.execute()

        # Vérifier si elle est terminée
        if self.current_strategy.est_terminee():
            self.finished = True
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
    
class StrategyZigZagObstacle(Strategy):
    def __init__(self, robot_adapter, env):
        super().__init__(robot_adapter)
        self.avancer = StrategyAvancer(robot_adapter)
        self.tourner = StrategyTourner(robot_adapter)
        self.etape = 0  # 0 = avancer, 1 = demi-tour
        self.compteur = 0
        self.max_tours = 10
        self.en_cours = True
        self.env=env

    def execute(self):
        if not self.en_cours:
            return

        # Étape 0 : avancer jusqu'à obstacle
        if self.etape == 0:
            obstacle_detecte, distance = self.robot_adapter.robot.capteurdistance()
            if (obstacle_detecte and distance < 30) :  # seuil de détection
                self.robot_adapter.set_speed_left(0)
                self.robot_adapter.set_speed_right(0)
                self.etape = 1
                self.tourner(180)  # Préparer la rotation
            else:
                self.avancer(1000, vitesse=50)  # avancer indéfiniment, sera interrompu par détection
                self.avancer.execute()

        # Étape 1 : faire demi-tour
        elif self.etape == 1:
            self.tourner.execute()
            if self.tourner.est_terminee():
                self.compteur += 1
                if self.compteur > self.max_tours:
                    self.en_cours = False
                    self.robot_adapter.set_speed_left(0)
                    self.robot_adapter.set_speed_right(0)
                    return
                self.etape = 0  # Reprendre l'avance

    def est_terminee(self):
        return not self.en_cours

class StrategieBleu(Strategy):
    def __init__(self, robot_adapter, simulation):
        super().__init__(robot_adapter)
        self.en_cours = True
        self.simulation=simulation

    def execute(self):
        if not self.en_cours:
            return
        self.simulation.b=True
        RobotAdapter.bleu()
        self.en_cours = False

    def est_terminee(self):
        return not self.en_cours
    
class StrategieRouge(Strategy):
    def __init__(self, robot_adapter,simulation):
        super().__init__(robot_adapter)
        self.en_cours = True
        self.simulation=simulation

    def execute(self):
        if not self.en_cours:
            return
        self.simulation.b=True
        RobotAdapter.rouge()
        self.en_cours = False

    def est_terminee(self):
        return not self.en_cours
    
class StrategieInvisible(Strategy):
    def __init__(self, robot_adapter,simulation):
        super().__init__(robot_adapter)
        self.en_cours = True
        self.simulation=simulation

    def execute(self):
        if not self.en_cours:
            return
        self.simulation.b=False
        self.en_cours = False

    def est_terminee(self):
        return not self.en_cours





