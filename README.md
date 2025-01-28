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

  ### Développement des obstacles
  - Création d'une classe mère 'Obstacle' définissant des méthodes générales (dessiner, est_dans) à implémenter dans les sous-classes.
  - Création d'une classe intermédiaire 'Forme' pour des formes géométriques, initialisée avec un centre (pos_x, pos_y)
  - Création des sous-classes dérivées de 'Forme':
      - Ellipse : Définie par un centre, un grand axe, et un petit axe.
      - Rectangle : Définie par un centre, une largeur, et une hauteur.
      - Triangle : Définie par trois sommets.
      - Ligne : Définie par deux points.
      Chaque sous-classe possède un constructeur spécifique et implémente les méthodes :
        - dessiner(ecran) : Dessine la forme sur l'écran.
        - est_dans(x, y) : Vérifie si un point (x,y) appartient à la forme.
  
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
