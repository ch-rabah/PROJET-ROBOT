import math
from Model.Robot import Robot
from Model.Obstacle import Rectangle, Cercle
from Model.Environnement import Environnement

class Simulation:
    def __init__(self):
        self.environnement = Environnement((0, 800), (0, 600))
        self.obstacles = [
            Rectangle((100, 100), (200, 50)),
            Cercle((500, 200), 30)
        ]
        for obstacle in self.obstacles:
            self.environnement.ajouter_obstacle(obstacle)

        self.robot = Robot(400, 300, direction=0, vitesse_gauche=0, vitesse_droite=0)

    def step(self, dt):
        """ Met à jour la simulation (déplacement du robot, détection de collisions) """

        self.robot.appliquer_vitesse_gauche(10)
        self.robot.appliquer_vitesse_droite(10)
        self.robot.avancer(dt)

        # Vérification des collisions
        for obstacle in self.environnement.obstacles:
            if obstacle.detecter_collision(self.robot):
                print("Collision détectée!")
                self.robot.arreter_robot()

                # Calcul de la direction de l'obstacle
                dx = obstacle.position[0] - self.robot.x
                dy = obstacle.position[1] - self.robot.y
                angle_robot = self.robot.direction
                angle_obstacle = math.atan2(dy, dx)
                delta_angle = (angle_obstacle - angle_robot + math.pi) % (2 * math.pi) - math.pi
                
                if -math.pi / 2 <= delta_angle <= math.pi / 2:
                    print("Obstacle devant, recul du robot")
                    self.robot.appliquer_vitesse_gauche(-5)
                    self.robot.appliquer_vitesse_droite(-5)
                else:
                    print("Obstacle derrière, le robot avance")
                    self.robot.appliquer_vitesse_gauche(5)
                    self.robot.appliquer_vitesse_droite(5)
                
                self.robot.avancer(dt)
                break  # Sortir dès qu'une collision est détectée

        if self.environnement.detecter_sorties(self.robot):
            print("Sortie du Monde détectée!")
            self.robot.arreter_robot()
        
        obstacle, distance = self.robot.cpadistance(self.environnement)
        if obstacle:
            print(f"Distance à l'obstacle : {distance}")

    def get_state(self):
        """ Renvoie l'état actuel de la simulation (robot et obstacles) """
        return self.robot, self.environnement