from ursina import *
from functools import singledispatchmethod
from model.obstacle import Rectangle, Cercle, Triangle, Ligne
import math
import time

HAUTEUR_OBSTACLE = 10
HAUTEUR_ROBOT = 2

class SimulationView3D:
    def __init__(self, environnement, robot):
        self.app = Ursina()  # Initialise l'application ici, sans super()

        self.environnement = environnement
        self.robot = robot

        window.title = "Simulation 3D Robot (Ursina)"
        window.borderless = False
        window.fullscreen = False
        window.exit_button.visible = True
        window.fps_counter.enabled = True
        window.color = color.gray

        # Délimiter l'environnement
        x_min, x_max = self.environnement.dimensions_x
        y_min, y_max = self.environnement.dimensions_y
        size_x = x_max - x_min
        size_z = y_max - y_min
        center_x = (x_max + x_min) / 2
        center_z = (y_max + y_min) / 2

        # Sol
        self.sol = Entity(
            model='plane',
            scale=(size_x, 1, size_z),  # Le sol doit avoir une hauteur (1)
            position=(center_x, 0, center_z),
            texture='white_cube',
            texture_scale=(size_x/10, size_z/10),
            color=color.white,
            collider='box'
        )

        # Objets
        self.robot_entity = Entity(model='cube', color=color.azure, scale=(5,5,5), position=(center_x,0.5,center_z), collider='box')
        self.obstacle_entities = []
        self.afficher_obstacles()
        self.afficher_balises()

        # Caméra orbitale qui tourne autour de l'environnement avec la souris
        self.camera = EditorCamera(position=(center_x, 20, center_z), rotation=(30, 45, 0))
        camera.ui.enabled = False
        self.camera1 = Entity(parent=self.robot_entity, position=(0, 1, 0), rotation=(0, 90, 0))
        self.etat_cam = 'editor'

        # Temps
        self.label = Text(text='', origin=(0, 18), background=True)

        # Gestion clavier par entité interne
        class InputHandler(Entity):
            def __init__(self, parent_view):
                super().__init__()
                self.parent_view = parent_view

            def input(self, key):
                if key == 'tab':
                    print(">> TAB détecté")
                    self.parent_view.switch()

        self.input_handler = InputHandler(self)

    def switch(self):
        if self.etat_cam == '1st':
            self.camera.enabled = True
            camera.parent = self.camera
            camera.world_position = self.camera.world_position
            camera.world_rotation = self.camera.world_rotation
            self.etat_cam = 'editor'
        else :
            self.camera.enabled = False
            camera.parent = self.camera1
            camera.world_position = self.camera1.world_position
            camera.world_rotation = self.camera1.world_rotation
            self.etat_cam = '1st'

    def afficher_infos(self, temps):
        texte = f"Temps écoulé : {temps:.2f} s\n"
        texte += f"Vitesse gauche : {self.robot.vitesse_gauche:.2f}\n"
        texte += f"Vitesse droite : {self.robot.vitesse_droite:.2f}"

        # Affichage dans le terminal
        print(texte)
        self.label.text = texte  # Mise à jour du texte

    def afficher_robot(self):
            # Mise à jour de la position et de la rotation du robot
            x, y = self.robot.x, self.robot.y
            angle = self.robot.direction
            self.robot_entity.position = (x, HAUTEUR_ROBOT, y)
            self.robot_entity.rotation_y = -math.degrees(angle)  # S'assurer de la bonne orientation

    @singledispatchmethod
    def afficher_obstacle(self, obstacle):
        raise TypeError(f"Type d'obstacle non géré: {type(obstacle)}")

    @afficher_obstacle.register
    def _(self, obstacle: Rectangle):
        x, y = obstacle.position
        l, h = obstacle.dimensions
        obj = Entity(
            model='cube',
            color=color.magenta,
            scale=(l, HAUTEUR_OBSTACLE, h),
            position=(x + l/2, HAUTEUR_OBSTACLE/2, y + h/2)
        )
        self.obstacle_entities.append(obj)

    @afficher_obstacle.register
    def _(self, obstacle: Cercle):
        x, y = obstacle.position
        r = obstacle.rayon
        # Utilisation du modèle 'sphere' pour représenter un cercle
        obj = Entity(
            model='sphere',  # Correctement écrit en minuscules
            color=color.magenta,
            scale=(r*2, HAUTEUR_OBSTACLE, r*2),  # Utilisation du rayon du cercle pour les dimensions X et Z
            position=(x, HAUTEUR_OBSTACLE/2, y)  # Positionner l'objet au centre, avec une hauteur ajustée
        )
        self.obstacle_entities.append(obj)

    @afficher_obstacle.register
    def _(self, obstacle: Ligne):
        x1, y1 = obstacle.point1
        x2, y2 = obstacle.point2
        dx, dz = x2 - x1, y2 - y1
        longueur = math.sqrt(dx**2 + dz**2)
        milieu = ((x1 + x2) / 2, (y1 + y2) / 2)
        obj = Entity(
            model='cube',
            color=color.magenta,
            scale=(longueur, HAUTEUR_OBSTACLE, obstacle.largeur),
            position=(milieu[0], HAUTEUR_OBSTACLE/2, milieu[1])
        )
        self.obstacle_entities.append(obj)

    @afficher_obstacle.register
    def _(self, obstacle: Triangle):
        sommets = obstacle.get_sommets()

        x1, y1 = sommets[0]
        x2, y2 = sommets[1]
        x3, y3 = sommets[2]

        h = HAUTEUR_OBSTACLE

        # Base (au sol)
        p1 = Vec3(x1, 0, y1)
        p2 = Vec3(x2, 0, y2)
        p3 = Vec3(x3, 0, y3)

        # Haut (même triangle mais élevé en Y)
        p4 = Vec3(x1, h, y1)
        p5 = Vec3(x2, h, y2)
        p6 = Vec3(x3, h, y3)

        # Construction du mesh avec faces latérales + haut + bas
        vertices = [p1, p2, p3, p4, p5, p6]
        triangles = [
            (0, 1, 2),  # base
            (3, 5, 4),  # haut
            (0, 3, 1), (1, 3, 4),  # côté 1
            (1, 4, 2), (2, 4, 5),  # côté 2
            (2, 5, 0), (0, 5, 3)   # côté 3
        ]

        mesh = Mesh(vertices=vertices, triangles=triangles, mode='triangle')
        obj = Entity(model=mesh, color=color.magenta)
        self.obstacle_entities.append(obj)

    def afficher_obstacles(self):
        for obs in self.environnement.obstacles:
            self.afficher_obstacle(obs)

    def afficher_balises(self):
        if not hasattr(self.environnement, "balises"):
            return

        for balise in self.environnement.balises:
            x, y = balise.position
            taille = balise.taille
            h = balise.hauteur
            rotation = balise.rotation
            couleurs = balise.couleurs

            # Créer un parent invisible à la bonne position et rotation
            parent = Entity(
                position=(x, h, y),
                rotation_y=rotation
            )

            # Offsets 2x2 centrés sur le parent
            offsets = [
                (-0.5, 0.5),  # haut gauche
                (0.5, 0.5),   # haut droite
                (-0.5, -0.5), # bas gauche
                (0.5, -0.5)   # bas droite
            ]

            for i in range(4):
                dx, dy = offsets[i]
                Entity(
                    parent=parent,  # attaché au parent
                    model='quad',
                    color=couleurs[i],
                    scale=(taille / 2, taille / 2),
                    position=(dx * taille / 2, dy * taille / 2, 0)
                    # pas de rotation ici → hérite de celle du parent
                )

    def mise_a_jour(self, temps):
        self.afficher_infos(temps)
        self.afficher_robot()
