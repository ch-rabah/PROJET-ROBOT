class Robot2I013:
    # Constantes physiques du robot
    WHEEL_BASE_WIDTH = 15.0  # Exemple en cm
    WHEEL_DIAMETER = 5.0  # Exemple en cm
    
    # Constantes pour le contrôle du robot
    MOTOR_LEFT = "left"
    MOTOR_RIGHT = "right"
    LED_EYE = "eye"
    LED_BLINKER = "blinker"
    
    def __init__(self):
        self.motor_speeds = {self.MOTOR_LEFT: 0, self.MOTOR_RIGHT: 0}
        self.wheel_positions = {self.MOTOR_LEFT: 0, self.MOTOR_RIGHT: 0}
    
    # Méthodes pour récupérer l'état du robot
    def get_voltage(self):
        print("get_voltage() exécuté")
        return 12.0  # Exemple de valeur fictive
    
    def get_image(self):
        print("get_image() exécuté")
        return None  # Placeholder pour une image
    
    def get_motor_position(self):
        print("get_motor_position() exécuté")
        return (self.wheel_positions[self.MOTOR_LEFT], self.wheel_positions[self.MOTOR_RIGHT])
    
    def get_distance(self):
        print("get_distance() exécuté")
        return 100.0  # Exemple de valeur fictive en cm
    
    # Méthodes pour contrôler le robot
    def set_led(self, led, r, g, b):
        print(f"set_led({led}, {r}, {g}, {b}) exécuté")
    
    def set_motor_dps(self, motor, dps):
        print(f"set_motor_dps({motor}, {dps}) exécuté")
        self.motor_speeds[motor] = dps
    
    def set_motor_encoder(self, motor, offset):
        print(f"set_motor_encoder({motor}, {offset}) exécuté")
        self.wheel_positions[motor] += offset
    
    def rotate_servo(self, port, angle):
        print(f"rotate_servo({port}, {angle}) exécuté")