from .strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle, StrategySuivreBalise


def initialiser_strategies(robot_adapter,coef_av=1,coef_tou=1,coef_dist=1):
    def condition_func_distance_proche():
        return robot_adapter.get_distance() < 40*coef_dist
    
    avancer = StrategyAvancer(robot_adapter,30*coef_av)
    tourner = StrategyTourner(robot_adapter,15*coef_tou)
    conditionnelle = StrategyConditionnelle(
        robot_adapter,
        (tourner, 90),      # si True, tourner de 90°
        (avancer, 30),      # si False, avancer de 30
        condition_func_distance_proche
    )
    suivre_balise = StrategySuivreBalise(robot_adapter)

    # Séquence avec réutilisation de la même instance de StrategyConditionnelle
    sequence = StrategySequentielle(robot_adapter, [
        (avancer, 20*coef_dist),
        (tourner, -90),
        (avancer, 20*coef_dist),
        (tourner, -90),
        (avancer, 20*coef_dist),
        (tourner, -90),
        (avancer, 20*coef_dist),
        (tourner, -90),
        (conditionnelle,(90,40*coef_dist)),
        (conditionnelle,(-90,50*coef_dist)),
        (suivre_balise, None),  
        
            
    ])
    
    return sequence

def verif_sequence(sequence):
    if not sequence.est_terminee():
            sequence.execute()
