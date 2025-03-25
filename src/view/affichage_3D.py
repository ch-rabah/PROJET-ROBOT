from ursina import *

class SimulationView3D:
    def __init__(self, environnement, robot):
        self.app = Ursina()

        self.environnement = environnement
        self.robot = robot

        # Créer un sol visible (gris avec quadrillage)
        self.ground = Entity(
            model='plane',
            scale=(100, 1, 100),
            color=color.gray,
            texture='white_cube',
            texture_scale=(50, 50),
            collider='box'
        )

        # Caméra en vue plongeante
        camera.position = (0, 60, -60)
        camera.look_at((0, 0, 0))

        # Lumière directionnelle
        DirectionalLight().look_at(Vec3(1, -1, -1))

        # Liste des entités à gérer plus tard
        self.robot_entity = None
        self.obstacle_entities = []
        self.trajet_entities = []

        # Pour afficher des infos à l'écran plus tard
        self.text_entity = None

    def run(self):
        """Lancer l'application Ursina"""
        self.app.run()

    def mise_a_jour(self, dt):
        """Méthode à appeler pour rafraîchir l'affichage"""
        # Pour l'instant, on affiche juste le temps à l'écran
        if self.text_entity:
            destroy(self.text_entity)

        self.text_entity = Text(
            text=f"Temps écoulé : {dt:.2f} s",
            position=(-0.85, 0.45),
            origin=(0, 0),
            scale=1.2,
            color=color.white
        )
