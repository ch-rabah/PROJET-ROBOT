from model.environnement import Environnement
from model.robot_3D import Robot
from model.obstacle_3D import Rectangle3D, Triangle3D, Ligne3D, Sphere3D
from view.affichage_3D import SimulationView3D


def main():
    # Créer l'environnement
    env = Environnement((0, 100), (0, 100))

    # Ajouter des obstacles
    env.ajouter_obstacle(Rectangle3D((20, 0, 20), (20, 1, 10)))
    env.ajouter_obstacle(Sphere3D((60, 0, 60), 5))
    env.ajouter_obstacle(Ligne3D((10, 0, 80), (90, 0, 80), largeur=1))
    env.ajouter_obstacle(Triangle3D((20, 0, 70), (30, 0, 90), (40, 0, 70)))


    # Créer le robot
    robot = Robot(x=50, y=50, environnement=env, direction=0)

    # Lancer l'affichage
    vue = SimulationView3D(env, robot)
    vue.run()


if __name__ == "__main__":
    main()
