from .strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle

def initialiser_strategies(robot_adapter):
    avancer = StrategyAvancer(robot_adapter)
    tourner = StrategyTourner(robot_adapter)
    

    # Séquence de stratégies
    sequence = StrategySequentielle(robot_adapter, [
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
        (StrategyAvancer, 30),
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
        (StrategyAvancer, 30),
    ])
    
    return sequence

def verif_sequence(sequence):
    if not sequence.est_terminee():
            print("Exécution de la stratégie séquentielle")
            sequence.execute()
