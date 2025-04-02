import time
from simulation_manager import initialiser_simulation, time_update, execution, up_env_simu_sleep


def main():
    # Initialiser la simulation
    environnement, robot, simulation, strategy_sequence, previous_time, tempsecouler = initialiser_simulation()

    # Boucle principale
    while True:
        dt, previous_time = time_update(previous_time)  # Récupérer dt et mettre à jour previous_time
        tempsecouler += dt
        execution(strategy_sequence)  # Passer dt à la fonction d'exécution
        up_env_simu_sleep(robot, dt, tempsecouler, environnement, simulation)


if __name__ == "__main__":
    main()
