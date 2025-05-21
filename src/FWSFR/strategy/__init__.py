from .strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle
def condition_func_distance_proche(robot_adapter):
    distance = robot_adapter.get_distance()
    print(f"[Condition] Distance détectée : {distance}")
    return distance < 20  # Seuil arbitraire

def initialiser_strategies(robot_adapter):
    avancer = StrategyAvancer(robot_adapter)
    tourner = StrategyTourner(robot_adapter)
    

    # Séquence de stratégies
    sequence = StrategySequentielle(robot_adapter, [
        (StrategyAvancer, 100),
        (StrategyTourner, 90),
        (StrategyAvancer, 100),
        (StrategyTourner, 90),
        (StrategyAvancer, 100),
        (StrategyTourner, 90),
        (StrategyAvancer, 100),
        (StrategyTourner, 90)
    ])
    
    return sequence

def verif_sequence(sequence):
    if not sequence.est_terminee():
            sequence.execute()
