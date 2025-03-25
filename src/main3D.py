import time
from model.environnement import Environnement
from model.robot_3D import Robot
from view.affichage_3D import SimulationView3D


def main():
    # Création de l’environnement (dimensions : 0 à 800 en X, 0 à 600 en Y)
    environnement = Environnement((0, 800), (0, 600))

    # Création du robot au centre de l’environnement
    robot = Robot(x=400, y=300, environnement=environnement, direction=0)

    # Création de la vue 3D
    simulation = SimulationView3D(environnement, robot)

    # Exemple de mise à jour manuelle : juste pour tester l'affichage
    temps_initial = time.time()

    def update():
        dt = time.time() - temps_initial
        simulation.mise_a_jour(dt)

    simulation.app.update = update  # Appeler mise_a_jour à chaque frame
    simulation.run()                # Lancer Ursina


if __name__ == "__main__":
    main()
