# Projet Robot

## Description du Projet

Ce projet consiste à développer un mini-robot équipé de capteurs et contrôleur, capable de se déplacer et d'éviter des obstacles. Le but principal est de tester les fonctionnalités du robot sur un simulateur avant de le mettre en mouvement réel.

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

  #### Développement des obstacles
  - Création d'une classe mère `Obstacle` définissant des méthodes générales (`dessiner`, `est_dans`) à implémenter dans les sous-classes.
  - Création d'une classe intermédiaire `Forme` pour des formes géométriques, initialisée avec un centre (pos_x, pos_y)
  - Création des sous-classes dérivées de `Forme`:
      - `Ellipse` : Définie par un centre, un grand axe, et un petit axe.
      - `Rectangle` : Définie par un centre, une largeur, et une hauteur.
      - `Triangle` : Définie par trois sommets.
      - `Ligne` : Définie par deux points.
      
    Chaque sous-classe possède un constructeur spécifique et implémente les méthodes :
    - `dessiner(ecran)` : Dessine la forme sur l'écran.
    - `est_dans(x, y)` : Vérifie si un point (x,y) appartient à la forme.
  
  #### Gestion graphique avec Pygame
  - Affichage d'un robot sous forme de triangle orienté en fonction de sa direction (`afficher_robot(robot)`).
  - Mise en place d'une boucle d'animation pour simuler les mouvements du robot.
  - Affichage dynamique des déplacements et rotations sur l'écran.
  - Affichage des obstacles avec la méthode `dessiner(ecran)` pour chaque sous-classe (`Ellipse`, `Rectangle`, `Triangle`, `Ligne`).


### Compte Rendu 2 : 
- **Date :** 05/02/2025
- **Résumé :**
  

  #### Développement du modèle de robot
  - Création d'une classe `Robot` avec les fonctionnalités suivantes :
    - Initialisation des paramètres (position, vitesse, accélération, direction).
    - Fonctionnalité de déplacement (`avancer(dt)`).
    - Rotation avec angle dynamique (`rotation()` et `tourner()`).
    - Mise à jour des vitesses selon l'accélération (`mettre_a_jour_vitesse()`).
    - Récupération des informations du robot (position, direction, vitesse).

  #### Développement des obstacles
  - Création d'une classe mère `Obstacle` définissant des méthodes générales (`dessiner`, `est_dans`) à implémenter dans les sous-classes.
  - Création d'une classe intermédiaire `Forme` pour des formes géométriques, initialisée avec un centre (pos_x, pos_y)
  - Création des sous-classes dérivées de `Forme`:
      - `Ellipse` : Définie par un centre, un grand axe, et un petit axe.
      - `Rectangle` : Définie par un centre, une largeur, et une hauteur.
      - `Triangle` : Définie par trois sommets.
      - `Ligne` : Définie par deux points.
      
    Chaque sous-classe possède un constructeur spécifique et implémente les méthodes :
    - `dessiner(ecran)` : Dessine la forme sur l'écran.
    - `est_dans(x, y)` : Vérifie si un point (x,y) appartient à la forme.

  #### Gestion graphique avec Pygame
  - Affichage d'un robot sous forme de triangle orienté en fonction de sa direction (`afficher_robot(robot)`).
  - Mise en place d'une boucle d'animation pour simuler les mouvements du robot.
  - Affichage dynamique des déplacements et rotations sur l'écran.
  - Affichage des obstacles avec la méthode `dessiner(ecran)` pour chaque sous-classe (`Ellipse`, `Rectangle`, `Triangle`, `Ligne`).

  #### Détails supplémentaires

  - **Modèle (Model.py)**
    - **Classe Robot** : Modélise un robot différentiel avec deux roues indépendantes. 
      - **Attributs clés** : Position `(x, y)` et direction en radians, vitesses des roues gauche et droite, distance entre les roues et taille du robot.
      - **Méthodes principales** :
        - `avancer(dt)` : Met à jour la position et la direction du robot en fonction du temps.
        - `appliquer_vitesse_gauche()` et `appliquer_vitesse_droite()` : Ajustent les vitesses des roues avec des limites maximales.
        - `decelerer_robot()` : Ralentit progressivement le robot pour atteindre l'arrêt.
        - `cpadistance()` : Détecte la distance à un obstacle en ligne droite devant le robot.

    - **Classe Obstacle** : Modélise des obstacles sous forme de rectangles et cercles, avec une méthode `detecter_collision()` pour vérifier les collisions avec le robot.
    - **Classe Environnement** : Gère les obstacles et définit les limites du monde.
      - Méthodes principales :
        - `ajouter_obstacle()` : Ajoute des obstacles à la simulation.
        - `detecter_sorties()` : Vérifie si le robot est sorti des limites définies.

  - **Vue (View.py)**
    - Affichage du robot sous forme de triangle (`afficher_robot()`) ou cercle (`afficher_robot2()`).
    - Affichage des obstacles et des informations du robot (`afficher_infos()`).

  - **Contrôleur (Control.py)**
    - Initialisation de Pygame et l'environnement (dimensions 800x600).
    - Ajout des obstacles (rectangulaire et circulaire).
    - Gestion des entrées utilisateur : Flèches Haut/Bas pour avancer/reculer, Flèches Gauche/Droite pour rotation sur place.
    - Arrêt progressif si aucune touche n'est pressée.
    - Vérification des collisions avec les obstacles et les sorties des limites.


### Compte Rendu 3  
- **Date :** 12/02/2025 
- **Résumé :**

  #### Séparation de la simulation et de la partie graphique
  - Changement de module, on passe de pygame à tkinter pour ça possible :
    - La simulation et l'affichage sont désormais distincts.  
    - Modifications du fichier `View.py` en conséquence.

  #### Refactorisation du modèle  
  - La classe `Model` a été divisée en trois fichiers distincts pour une meilleure organisation :  
    - **`Robot.py`** : Contient la classe `Robot`, la vitesse et les mouvements. Améliorations de la fonction `cpadistance()` pour qu'elle ne dépende plus de la création d'un robot. 
    - **`Obstacles.py`** : Définit la classe mère `Obstacle` et les différentes formes géométriques.  
    - **`Environnement.py`** : Gère l’ensemble des obstacles et leur interaction avec le robot.  

  #### Ajout des nouvelles formes d'obstacles  
  - Création des sous-classes d'obstacles `Ligne` et `Triangle`. 
  - Chaque classe implémente :  
    - Un **constructeur** spécifique.   
    - Une méthode `detecter_collision()` pour vérifier la présence d’un point dans la forme.  

  #### Ajout des tests unitaires  
  - Mise en place de tests unitaires avec `assert` pour valider le bon fonctionnement des méthodes :  
    - Vérification des déplacements et rotations du robot.  
    - Test des collisions entre le robot et les obstacles.  
    - Validation des méthodes de dessin et de détection de points dans les formes.  



## Bibliographie

1. **pygame** https://pypi.org/project/pygame/
   - Bibliothèque pygame
  
2. **math** https://docs.python.org/3/library/math.html
   - Bibliothèque math

3. **tkinter** https://docs.python.org/fr/3/library/tkinter.html
   - Bibliothèque tkinter

---
