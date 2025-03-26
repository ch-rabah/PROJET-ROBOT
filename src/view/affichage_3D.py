from vpython import *
import time
from view.camera_orbitale import CameraOrbitale

class SimulationView3D:
    def __init__(self, environnement, robot):
        self.environnement = environnement
        self.robot = robot
        self.scene = canvas(title="Simulation 3D Robot", width=800, height=600, center=vector(0, 0, 0), background=color.gray(0.2))

        # Créer un sol quadrillé
        self.sol = box(pos=vector(0, -0.1, 0), size=vector(100, 0.1, 100), color=color.white, opacity=0.5)

        # Initialisation de la caméra orbitale
        self.camera_orbitale = CameraOrbitale(scene=self.scene, target=vector(0, 0, 0))

        # Texte d'information (en haut à gauche de l'écran)
        self.info_label = label(pos=vector(0, 0, 0), text='', xoffset=-self.scene.width//2 + 60, yoffset=self.scene.height//2 - 40,
                                height=14, border=4, font='sans', box=False, color=color.white, line=False, space=30, screen=True)

    def afficher_infos(self, temps):
        texte = f"Temps écoulé : {temps:.2f} s\n"
        texte += f"Vitesse gauche : {self.robot.vitesse_gauche:.2f}\n"
        texte += f"Vitesse droite : {self.robot.vitesse_droite:.2f}"
        self.info_label.text = texte

    def afficher_robot(self):
        if hasattr(self, 'objet_robot'):
            self.objet_robot.visible = False
        self.objet_robot = box(
            pos=vector(self.robot.x, self.robot.taille_robot / 2, self.robot.z),
            size=vector(self.robot.taille_robot, self.robot.taille_robot, self.robot.taille_robot),
            color=color.blue
        )

    def mise_a_jour(self, temps):
        self.afficher_infos(temps)
        self.camera_orbitale.update()
        self.afficher_robot()

    def run(self):
        t0 = time.time()
        while True:
            rate(60)
            t = time.time() - t0
            self.mise_a_jour(t)
