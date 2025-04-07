import time
from tkinter import Tk
from src.view.affichage_Tkinter import SimulationView
from src.model.robot import Robot
from src.model.environnement import Environnement
from src.model.obstacle import Rectangle, Cercle, Ligne, Triangle
from src.strategy.strategy import StrategyAvancer, StrategyTourner, StrategyConditionnelle, StrategySequentielle
from src.adapter.adapter import RobotAdapterSimulation , RobotAdapterReel
from src.RobotReel.Robot2I013 import Robot2I013