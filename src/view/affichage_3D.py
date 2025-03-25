from vpython import *
from view.camera_orbitale import CameraOrbitale
import time

class SimulationView3D:
    def __init__(self, environnement, robot):
        self.environnement = environnement
        self.robot = robot
        self.scene = canvas(title="Simulation 3D Robot", width=800, height=600, center=vector(0, 0, 0), background=color.gray(0.2))

        # Créer un sol quadrillé
        self.sol = box(pos=vector(0, -0.1, 0), size=vector(100, 0.1, 100), color=color.white, opacity=0.5)

        # Initialisation de la caméra orbitale
        self.camera_orbitale = CameraOrbitale(scene=self.scene, target=vector(0, 0, 0))

        # Texte d'information (temporaire)
        self.info_label = label(pos=vector(0, 10, 0), text='', xoffset=0, yoffset=0, space=30, height=16, border=4, font='sans')

    def mise_a_jour(self, temps):
        # Mise à jour du texte à l'écran
        self.info_label.text = f"Temps écoulé : {temps:.2f} s"
        self.camera_orbitale.update()

    def run(self):
        t0 = time.time()
        while True:
            rate(60)
            t = time.time() - t0
            self.mise_a_jour(t)
