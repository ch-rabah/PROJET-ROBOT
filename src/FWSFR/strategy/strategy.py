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
    """
    Stratégie pour faire avancer le robot en ligne droite sur une distance donnée.
    Utilise une vitesse fixe, et s’arrête automatiquement lorsque la distance cible est atteinte.
    """
    def __init__(self, robot_adapter,vitesse):
        """
        :param robot_adapter: L'adapter du robot (passé pour compatibilité)
        :param vitesse: Vitesse de déplacement du robot 
        """
        super().__init__(robot_adapter)
        self.distance_cible = 0
        self.vitesse = vitesse

    def execute(self):
        """Exécute la stratégie d'avancement.
        - Vérifie si la distance cible est atteinte.
        - Si non, avance le robot à la vitesse définie.
        - Si la distance cible est atteinte, arrête le robot et affiche un message.
        """
        self.robot_adapter.set_speed_left(self.vitesse)
        self.robot_adapter.set_speed_right(self.vitesse)     

        # Vérifier si la distance cible est atteinte
        if self.robot_adapter.calculer_distance_parcourue() >= self.distance_cible:
            print(f"Distance cible atteinte ({self.robot_adapter.calculer_distance_parcourue():.2f} mm)")
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)

    def __call__(self, distance_cible):
        self.distance_cible = distance_cible

    def est_terminee(self):
        """Vérifie si la stratégie d'avancement est terminée.
        Retourne True si la distance cible est atteinte, sinon False.
        """
        if self.robot_adapter.calculer_distance_parcourue() >= self.distance_cible:  # Retourne True si l'objectif est atteint
            self.robot_adapter.reset()
            return True
        return False

class StrategyTourner(Strategy):
    """
    Stratégie permettant de faire tourner le robot sur place d’un angle donné (en degrés).
    Le robot tourne à une vitesse fixée, et s’arrête lorsque l’angle cible est atteint.
    """
    def __init__(self, robot_adapter,vitesse):
        """
        :param robot_adapter: L'adapter du robot (passé pour compatibilité)
        :param vitesse: Vitesse de rotation du robot 
        """
        super().__init__(robot_adapter)
        self.angle_cible = 0
        self.vitesse = vitesse

    def execute(self):
        """Exécute la stratégie de rotation.
        - Vérifie si l'angle cible est atteint.
        - Si non, fait tourner le robot à la vitesse définie.
        - Si l'angle cible est atteint, arrête le robot et affiche un message.
        """
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

    def __call__(self, angle_cible):
        self.angle_cible = angle_cible

    def est_terminee(self):
        """Vérifie si la stratégie de rotation est terminée.
        Retourne True si l'angle cible est atteint, sinon False.
        """
        if abs(self.robot_adapter.calculer_angle_parcouru()) >= abs(self.angle_cible):
            self.robot_adapter.reset()
            return True
        return False

class StrategyConditionnelle(Strategy):
    """Stratégie conditionnelle qui choisit entre deux stratégies en fonction d'une condition.
    - Si la condition est vraie, utilise strategy1 avec param1.
    - Si la condition est fausse, utilise strategy2 avec param2.
    La stratégie s'arrête lorsque l'une des deux stratégies est terminée.
    """

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
        """
        Exécute la stratégie conditionnelle.
        - Si la stratégie actuelle est terminée, on passe à l'autre.
        - Si aucune stratégie n'est en cours, on vérifie la condition et on choisit la stratégie appropriée.
        """
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
        """Vérifie si la stratégie conditionnelle est terminée."""
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
        """ Exécute la stratégie séquentielle.
        - Passe à la stratégie suivante si la stratégie actuelle est terminée.
        - Exécute la stratégie actuelle.
        - Si toutes les stratégies sont terminées, ne fait rien.
        """
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
        """Vérifie si toutes les stratégies de la séquence sont terminées.
        Retourne True si toutes les stratégies ont été exécutées et sont terminées."""
        return self.current_strategy_index >= len(self.strategies)



class StrategySuivreBalise(Strategy):
    """
    Stratégie de suivi de balise : le robot ajuste ses vitesses pour garder la balise au centre de sa vision.
    Si la balise est perdue ou non détectée, la stratégie s’arrête.
    """
    def __init__(self, robot_adapter):
        """
        :param robot_adapter: L'adapter du robot (passé pour compatibilité)
        """
        super().__init__(robot_adapter)
        self.terminee = False

    def __call__(self):
        self.terminee = False

    def execute(self):
        """Exécute la stratégie de suivi de balise.
        - Récupère l'image du robot.
        - Génère un masque pour détecter la balise.
        - Détermine la position de la balise dans l'image.
        - Ajuste les vitesses du robot en fonction de la position de la balise.
        - Si la balise n'est pas détectée, arrête le robot et marque la stratégie comme terminée.
        """
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
                self.robot_adapter.set_speed_left(20)
                self.robot_adapter.set_speed_right(50)
            elif position == "droite":
                self.robot_adapter.set_speed_left(50)
                self.robot_adapter.set_speed_right(20)
            else:
                self.robot_adapter.set_speed_left(50)
                self.robot_adapter.set_speed_right(50)

    def est_terminee(self):
        """Vérifie si la stratégie de suivi de balise est terminée.
        Retourne True si la balise n'est pas détectée ou si la stratégie a été arrêtée.
        """
        return self.terminee

class StrategyUnDeuxTroisSoleil(Strategy):
    """
    1, 2, 3 soleil : le robot avance tant qu'il voit la balise,
    s'arrête quand il ne la voit plus,
    la stratégie se termine uniquement quand il est vraiment proche de la balise (capteur de distance).
    """
    def __init__(self, robot_adapter, vitesse=40, distance_cible=20):
        """
        :param robot_adapter: L'adapter du robot (passé pour compatibilité)
        :param vitesse: Vitesse de déplacement du robot (par défaut 40)
        :param distance_cible: Distance cible à atteindre pour considérer la balise comme proche (par défaut 20 cm)
        """
        super().__init__(robot_adapter)
        self.terminee = False
        self.vitesse = vitesse
        self.distance_cible = distance_cible  # cm

    def __call__(self, vitesse=None, distance_cible=None):
        """ Réinitialise la stratégie avec de nouveaux paramètres.
        :param vitesse: Nouvelle vitesse de déplacement (par défaut None, utilise la valeur actuelle)
        :param distance_cible: Nouvelle distance cible à atteindre (par défaut None, utilise la valeur actuelle)
        """
        if vitesse is not None:
            self.vitesse = vitesse
        if distance_cible is not None:
            self.distance_cible = distance_cible
        self.terminee = False

    def execute(self):
        """Exécute la stratégie 1, 2, 3 soleil.
        - Vérifie si la stratégie est déjà terminée.
        - Vérifie la distance à l'obstacle/balise devant.
        - Si la distance est inférieure à la distance cible, arrête le robot et marque la stratégie comme terminée.
        - Récupère l'image du robot.
        - Génère un masque pour détecter la balise.
        - Détermine la position de la balise dans l'image.
        - Si la balise est visible, avance le robot.
        - Si la balise n'est pas visible, arrête le robot et attend qu'elle revienne.
        """
        if self.terminee:
            return

        # Vérification de la distance
        distance = self.robot_adapter.get_distance()  # récupère la distance à l'obstacle/balise devant
        if distance is not None and distance < self.distance_cible:
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)
            print("Balise très proche : victoire !")
            self.terminee = True
            return

        image = self.robot_adapter.get_image()
        if image is None:
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)
            return

        masque = generer_masque_balise(image)
        position = position_balise_dans_image(masque)

        if position is None:
            # Pas de balise visible : STOP, mais on attend qu'elle revienne
            self.robot_adapter.set_speed_left(0)
            self.robot_adapter.set_speed_right(0)
        else:
            # Balise vue : on avance
            self.robot_adapter.set_speed_left(self.vitesse)
            self.robot_adapter.set_speed_right(self.vitesse)

    def est_terminee(self):
        return self.terminee
