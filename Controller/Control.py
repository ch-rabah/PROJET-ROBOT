

def evitemment(environnement, robot,dt):
    global EVITER
    obstacle, distance = robot.cpadistance(environnement)

    if obstacle:
        
        if distance < 50:  # Distance critique → Freiner et reculer
            robot.appliquer_vitesse_gauche(-(robot.vitesse_gauche/2))
            robot.appliquer_vitesse_droite(-(robot.vitesse_gauche/2))
            EVITER = True  


        elif distance < 30:  # Distance de sécurité → Tourner pour éviter
            if robot.vitesse_gauche > robot.vitesse_droite:
                # Si déjà en train de tourner à gauche, accentuer l'évitement
                robot.appliquer_vitesse_gauche(10)
                robot.appliquer_vitesse_droite(70)
            else:
                # Sinon, tourner à droite
                robot.appliquer_vitesse_gauche(70)
                robot.appliquer_vitesse_droite(10)
            EVITER = True  

    elif EVITER:  # Une fois l'obstacle évité, rétablir la trajectoire
        robot.appliquer_vitesse_gauche(-robot.vitesse_gauche)
        robot.appliquer_vitesse_droite(-robot.vitesse_droite)
        EVITER = False

