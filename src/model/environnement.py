import math

class Environnement:
    def __init__(self, dimX=None, dimY=None):
        self.obstacles = []  # Liste d'objets Obstacle stockés dans l'environnement
        self.dimensions_x = dimX  # Largeur totale du monde
        self.dimensions_y = dimY  # Hauteur totale du monde
    
    def ajouter_obstacle(self, obstacle):
        """Ajoute un obstacle à l'environnement"""
        self.obstacles.append(obstacle)

    def detecter_sorties(self, robot):
        """
        Vérifie si le robot est en dehors des limites du monde.
        Si oui, retourne True pour indiquer une sortie.
        Sinon, retourne False.
        """
        # Position et taille du robot
        rx = robot.x
        ry = robot.y
        taille_robot = robot.taille_robot
        base_triangle = robot.taille_robot
        direction = robot.direction
        point1 = (
            rx + base_triangle * math.cos(direction - math.pi / 2),
            ry + base_triangle * math.sin(direction - math.pi / 2)
        )
        point2 = (
            rx + base_triangle * math.cos(direction + math.pi / 2),
            ry + base_triangle * math.sin(direction + math.pi / 2)
        )
        point3 = (
            rx + taille_robot * math.cos(direction + math.pi),
            ry + taille_robot * math.sin(direction + math.pi)
        )

        # Dimensions du monde
        min_x, max_x = self.dimensions_x
        min_y, max_y = self.dimensions_y

        # Vérifier si le robot est en dehors des limites du monde
        for x, y in [point1, point2, point3, (rx, ry)]:
            if x < min_x or x > max_x or y < min_y or y > max_y:
                return True
        return False

    def gerer_collisions(self, robot):
        """
        Gère les collisions avec les obstacles et la sortie de l'environnement.
        """
        for obstacle in self.obstacles:
            collision = obstacle.detecter_collision(robot)
            if collision:
                print("Collision détectée!")
                robot.appliquer_vitesse_gauche(0)
                robot.appliquer_vitesse_droite(0)

                dx = obstacle.position[0] - robot.x
                dy = obstacle.position[1] - robot.y
                angle_robot = robot.direction
                angle_obstacle = math.atan2(dy, dx)
                delta_angle = (angle_obstacle - angle_robot + math.pi) % (2 * math.pi) - math.pi

                if -math.pi / 2 <= delta_angle <= math.pi / 2:
                    robot.appliquer_vitesse_gauche(-5)
                    robot.appliquer_vitesse_droite(-5)
                else:
                    robot.appliquer_vitesse_gauche(5)
                    robot.appliquer_vitesse_droite(5)

                break

        # Empêcher le robot de sortir des limites de l'environnement
        min_x, max_x = self.dimensions_x
        min_y, max_y = self.dimensions_y
        if robot.x < min_x:
            robot.x = min_x
            robot.appliquer_vitesse_gauche(0)
            robot.appliquer_vitesse_droite(0)
        elif robot.x > max_x:
            robot.x = max_x
            robot.appliquer_vitesse_gauche(0)
            robot.appliquer_vitesse_droite(0)
        if robot.y < min_y:
            robot.y = min_y
            robot.appliquer_vitesse_gauche(0)
            robot.appliquer_vitesse_droite(0)
        elif robot.y > max_y:
            robot.y = max_y
            robot.appliquer_vitesse_gauche(0)
            robot.appliquer_vitesse_droite(0)

    def update(self, robot, dt):
        """
        Met à jour l'état de l'environnement en gérant les collisions et en détectant les sorties.
        """
        if self.detecter_sorties(robot):
            print("Le robot est sorti des limites de l'environnement!")
            robot.appliquer_vitesse_gauche(0)
            robot.appliquer_vitesse_droite(0)
        self.gerer_collisions(robot)
        robot.mise_a_jour_robot(dt)