import time
from model.environnement import Environnement
from model.robot import Robot
from model.obstacle import Rectangle, Triangle, Ligne, Cercle
from model.balise import Balise
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle
from adapter.adapter import RobotAdapterSimulation
from view.affichage_3D import SimulationView3D

# Fonction conditionnelle (exemple : après 5 secondes, la condition devient vraie)
def condition_func():
    global start_time
    current_time = time.time()
    elapsed_time = current_time - start_time
    print(f"Temps écoulé : {elapsed_time:.2f} secondes")  # Affiche le temps écoulé pour le débogage

    if elapsed_time > 3:  # Condition : après 3 secondes, retourne True
        print("Condition remplie : True")
        return True
    print("Condition non remplie : False")
    return False

def main():
    global start_time
    start_time = time.time()  # Temps de départ pour la condition
    
    print("Début du programme, start_time initialisé à :", start_time)
    
    # Initialisation de l'environnement et du robot
    env = Environnement((0, 200), (0, 200))
    env.ajouter_obstacle(Rectangle((20, 20), (20, 10)))
    env.ajouter_obstacle(Cercle((60, 120), 5))
    env.ajouter_obstacle(Ligne((20, 160), (180, 160), largeur=1))
    env.ajouter_obstacle(Triangle((20, 70), (30, 90), (40, 70)))
    env.ajouter_balise(Balise(position=(110, 130), taille=10, hauteur=5, rotation=45))

    # Création du robot et de l'adaptateur
    robot = Robot(x=100, y=100, environnement=env, direction=0)
    robot_adapter = RobotAdapterSimulation(robot)
    
    # Initialisation de la simulation 3D
    simulation = SimulationView3D(env, robot)

    # Définition des stratégies
    avancer = StrategyAvancer(robot_adapter)
    tourner = StrategyTourner(robot_adapter)

    # Stratégie conditionnelle : exécute la première stratégie (avancer) ou la deuxième (tourner) selon la condition
    strategy_conditionnelle = StrategyConditionnelle(
        robot_adapter,
        (StrategyAvancer, 30),  # Avancer de 30 unités si la condition est vraie
        (StrategyTourner, 90),  # Tourner de 90 degrés si la condition est fausse
        condition_func  # Condition qui vérifie si le temps écoulé est supérieur à 3 secondes
    )

    # Séquence de stratégies (avancer puis tourner)
    sequence = StrategySequentielle(robot_adapter, [
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
        (StrategyAvancer, 30),
    ])

    previous_time = time.time()
    elapsed_time = 0

    while True:
        now = time.time()
        dt = now - previous_time
        previous_time = now
        elapsed_time += dt

        # Exécution de la stratégie conditionnelle
        if not strategy_conditionnelle.est_terminee():
            print("Exécution de la stratégie conditionnelle")
            strategy_conditionnelle.execute()

        # Exécution de la séquence de stratégies si la stratégie conditionnelle est terminée
        elif not sequence.est_terminee():
            print("Exécution de la stratégie séquentielle")
            sequence.execute()

        # Mettre à jour l'environnement et la simulation 3D
        env.update(robot, dt)
        simulation.mise_a_jour(elapsed_time)
        simulation.app.step()
        time.sleep(1/60)

if __name__ == "__main__":
    main()
