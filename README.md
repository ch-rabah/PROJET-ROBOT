# Projet Robot

## Description du Projet

Le projet consiste à réaliser un programme qui servira à faire bouger un mini-robot. L'objectif principal est de tester les différentes fonctions sur un simulateur avant le test physique dans le lequel on implémentera le code.

### Objectifs principaux :
- Tracer un carré
- S'approcher le plus vite possible et le plus près d'un mur sans le toucher
- Suivre une balise

### Composition du robot :
- Un Raspberry Pi
- Une carte contrôleur (arduino)
- Deux moteurs encodeurs pour le contrôle des roues
- 3 senseurs : une caméra, un capteur de distance et un accéléromètre

---

## Comptes Rendus

### Compte Rendu 1 : 
- **Date :** 27/01/2025
- **Résumé :**
  #### Développement du modèle de robot
  - Création d'une classe `Robot` avec les fonctionnalités suivantes :
    - Initialisation des paramètres (position, vitesse, accélération, direction).
    - Fonctionnalité de déplacement (`avancer(dt)`).
    - Rotation avec angle dynamique (`rotation()` et `tourner()`).
    - Mise à jour des vitesses selon l'accélération (`mettre_a_jour_vitesse()`).
    - Récupération des informations du robot (position, direction, vitesse).
  
  #### Gestion graphique avec Pygame
  - Affichage d'un robot sous forme de triangle orienté en fonction de sa direction (`afficher_robot(robot)`).
  - Mise en place d'une boucle d'animation pour simuler les mouvements du robot.
  - Affichage dynamique des déplacements et rotations sur l'écran.

- 

---

## Bibliographie

1. **pygame** https://pypi.org/project/pygame/
   - Bibliothèque pygame
  
1. **math** https://docs.python.org/3/library/math.html
   - Bibliothèque math

---
