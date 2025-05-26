from .strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle, StrategySuivreBalise


def initialiser_strategies(robot_adapter):
    def condition_func_distance_proche():
        return robot_adapter.get_distance() < 40
    
    avancer = StrategyAvancer(robot_adapter)
    tourner = StrategyTourner(robot_adapter)
    conditionnelle = StrategyConditionnelle(
        robot_adapter,
        (tourner, 90),      # si True, tourner de 90°
        (avancer, 30),      # si False, avancer de 30
        condition_func_distance_proche
    )
    suivre_balise = StrategySuivreBalise(robot_adapter)

    # Séquence avec réutilisation de la même instance de StrategyConditionnelle
    sequence = StrategySequentielle(robot_adapter, [
        (avancer, 30),
        (tourner, 90),
        (suivre_balise, None),  
        
            
    ])
    
    return sequence

def verif_sequence(sequence):
    if not sequence.est_terminee():
            sequence.execute()
