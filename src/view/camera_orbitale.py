from vpython import scene, vector, keysdown
import math
import time

class CameraOrbitale:
    def __init__(self, scene, target=vector(0, 0, 0), distance=70, angle=(math.pi/4, math.pi/6)):
        self.scene = scene
        self.target = target
        self.distance = distance
        self.angle = list(angle)  # [azimut, élévation]
        self.enabled = True
        self.last_time = time.time()
        self.update_camera()

    def update(self):
        if not self.enabled:
            return

        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Contrôle clavier
        keys = keysdown()
        if 'left' in keys:
            self.angle[0] -= 1.5 * dt
        if 'right' in keys:
            self.angle[0] += 1.5 * dt
        if 'up' in keys:
            self.distance -= 30 * dt
        if 'down' in keys:
            self.distance += 30 * dt

        self.distance = max(10, min(200, self.distance))
        self.angle[1] = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle[1]))

        self.update_camera()

    def update_camera(self):
        phi = self.angle[0]   # horizontal
        theta = self.angle[1]  # vertical

        x = self.distance * math.cos(theta) * math.sin(phi)
        y = self.distance * math.sin(theta)
        z = self.distance * math.cos(theta) * math.cos(phi)

        self.scene.camera.pos = self.target + vector(x, y, z)
        self.scene.camera.axis = self.target - self.scene.camera.pos
