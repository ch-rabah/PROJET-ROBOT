# simulation_manager.py
import time
from adapter.adapter import RobotAdapterSimulation
from model.robot import Robot
from model.environnement import Environnement
from model.obstacle import Rectangle, Cercle, Ligne, Triangle
from strategy.strategy import StrategySequentielle, StrategyAvancer, StrategyTourner
from view.affichage_Tkinter import SimulationView
from tkinter import Tk

def initialiser_simulation():
    """Initialise tous les objets nécessaires à la simulation."""
    # Initialisation de l'environnement et du robot
    environnement = Environnement((0, 800), (0, 600))
    robot = Robot(400, 300, environnement=environnement)

    environnement.ajouter_obstacle(Rectangle((100, 100), (200, 50)))
    environnement.ajouter_obstacle(Triangle((600, 300), (650, 350), (700, 300)))

    robot_adapter = RobotAdapterSimulation(robot)

    # Création de l'affichage
    simulation = SimulationView(Tk(), environnement, robot)

    # Définition des stratégies
    strategy_sequence = StrategySequentielle(
        robot_adapter,
        [(StrategyAvancer, 100), (StrategyTourner, 90)] * 4
    )

    previous_time = time.time()
    tempsecouler = 0

    return environnement, robot, simulation, strategy_sequence, previous_time, tempsecouler

def execution(strategy_sequence):
    """Exécuter la stratégie conditionnelle une fois que les stratégies fixes sont terminées"""
    if not strategy_sequence.est_terminee():
        strategy_sequence.execute()  # Passer dt à execute()

def time_update(previous_time):
    current_time = time.time()
    dt = current_time - previous_time
    previous_time = current_time
    
    return dt, previous_time  # Retourner le dt et previous_time mis à jour

def up_env_simu_sleep(robot, dt, tempsecouler, environnement, simulation):
    environnement.update(robot, dt)
    simulation.mise_a_jour(tempsecouler)
    time.sleep(1 / 60)
