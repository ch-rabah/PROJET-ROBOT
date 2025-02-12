from Model.Environnement import Environnement
from Model.Robot import Robot
from Model.Obstacle import Rectangle, Cercle, Ligne, Triangle

### TEST ENVIRONNEMENT ###
env = Environnement((0, 800), (0, 600))
assert env.dimensions_x == (0, 800), "Erreur : dimensions X incorrectes"
assert env.dimensions_y == (0, 600), "Erreur : dimensions Y incorrectes"
assert len(env.obstacles) == 0, "Erreur : la liste des obstacles devrait être vide"

### TEST OBSTACLES ###
rect = Rectangle((100, 100), (200, 50))
cercle = Cercle((400, 300), 50)
ligne = Ligne((50, 50), (70, 70))
triangle = Triangle((500, 100), (600, 150), (550, 250))

env.ajouter_obstacle(rect)
env.ajouter_obstacle(cercle)
env.ajouter_obstacle(ligne)
env.ajouter_obstacle(triangle)

assert len(env.obstacles) == 4, "Erreur : le nombre d'obstacles est incorrect"
assert rect in env.obstacles, "Erreur : le rectangle n'a pas été ajouté"
assert cercle in env.obstacles, "Erreur : le cercle n'a pas été ajouté"
assert ligne in env.obstacles, "Erreur : la ligne n'a pas été ajoutée"
assert triangle in env.obstacles, "Erreur : le triangle n'a pas été ajouté"

### TEST ROBOT ###
robot = Robot(400, 300, direction=0)
assert robot.x == 400 and robot.y == 300, "Erreur : position initiale du robot incorrecte"
assert robot.vitesse_gauche == 0 and robot.vitesse_droite == 0, "Erreur : vitesse initiale incorrecte"

# Application de vitesse
robot.appliquer_vitesse_gauche(50)
assert robot.vitesse_gauche == 50, "Erreur : vitesse gauche incorrecte"

robot.appliquer_vitesse_droite(60)
assert robot.vitesse_droite == 60, "Erreur : vitesse droite incorrecte"

# Arrêt du robot
robot.arreter_robot()
assert robot.vitesse_gauche == 0 and robot.vitesse_droite == 0, "Erreur : le robot ne s'est pas arrêté"

# Avancer
robot.appliquer_vitesse_gauche(50)
robot.appliquer_vitesse_droite(50)
robot.avancer(1)
assert 445 <= robot.x <= 455, "Erreur : la position X après déplacement est incorrecte"
assert 295 <= robot.y <= 305, "Erreur : la position Y après déplacement est incorrecte"

# Détection des sorties
robot.x, robot.y = 900, 700  # Hors des limites
assert env.detecter_sorties(robot), "Erreur : le robot aurait dû être détecté hors des limites"

robot.x, robot.y = 400, 300  # De retour dans l'environnement
assert not env.detecter_sorties(robot), "Erreur : le robot ne devrait pas être considéré comme hors des limites"

### TEST COLLISIONS OBSTACLES ###
# On place le robot au même endroit qu'un obstacle pour tester la collision
robot.x, robot.y = 150, 125  # À l'intérieur du rectangle
assert rect.detecter_collision((robot.x, robot.y)), "Erreur : le robot devrait être en collision avec le rectangle"

robot.x, robot.y = 400, 300  # Au centre du cercle
assert cercle.detecter_collision((robot.x, robot.y)), "Erreur : le robot devrait être en collision avec le cercle"

robot.x, robot.y = 550, 150  # À l'intérieur du triangle
assert triangle.detecter_collision((robot.x, robot.y)), "Erreur : le robot devrait être en collision avec le triangle"

robot.x, robot.y = 55, 55  # Sur la ligne
assert ligne.detecter_collision((robot.x, robot.y)), "Erreur : le robot devrait être en collision avec la ligne"

# Vérification qu'il n'y a PAS de collision en dehors des obstacles
robot.x, robot.y = 700, 500  # Zone vide
assert not rect.detecter_collision((robot.x, robot.y)), "Erreur : mauvaise détection de collision avec le rectangle"
assert not cercle.detecter_collision((robot.x, robot.y)), "Erreur : mauvaise détection de collision avec le cercle"
assert not triangle.detecter_collision((robot.x, robot.y)), "Erreur : mauvaise détection de collision avec le triangle"
assert not ligne.detecter_collision((robot.x, robot.y)), "Erreur : mauvaise détection de collision avec la ligne"

print(" Tous les tests sont passés avec succès ! ")
