from model.environnement import Environnement
from model.robot_3D import Robot
from view.affichage_3D import SimulationView3D


def main():
    # Création d’un environnement simple
    environnement = Environnement((0, 100), (0, 100))

    # Création du robot (même s'il n'est pas encore affiché)
    robot = Robot(x=0, y=0, environnement=environnement, direction=0)

    # Lancement de la simulation 3D avec VPython
    simulation = SimulationView3D(environnement, robot)
    simulation.run()


if __name__ == "__main__":
    main()
