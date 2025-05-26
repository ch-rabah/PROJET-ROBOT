import cv2
import numpy as np

# Plages HSV pour chaque couleur de la balise
PLAGES_HSV = {
    "jaune": ((20, 100, 100), (35, 255, 255)),
    "vert":  ((40, 50, 50),   (85, 255, 255)),
    "rouge1": ((0, 100, 100), (10, 255, 255)),
    "rouge2": ((160, 100, 100), (180, 255, 255)),
    "bleu":  ((100, 100, 100), (130, 255, 255))
}

# Charger l'image (mets ici le chemin vers ta photo)
img = cv2.imread(r"C:\Users\wassi\Documents\env_projet_robot\PROJET-ROBOT\src\FWSFR\algo_detection\photo7.jpg")
if img is None:
    print("Erreur : impossible de charger l’image !")
    exit()

# Conversion BGR -> HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Création des masques couleur
mask_jaune = cv2.inRange(hsv, np.array(PLAGES_HSV["jaune"][0]), np.array(PLAGES_HSV["jaune"][1]))
mask_vert = cv2.inRange(hsv, np.array(PLAGES_HSV["vert"][0]), np.array(PLAGES_HSV["vert"][1]))
mask_rouge1 = cv2.inRange(hsv, np.array(PLAGES_HSV["rouge1"][0]), np.array(PLAGES_HSV["rouge1"][1]))
mask_rouge2 = cv2.inRange(hsv, np.array(PLAGES_HSV["rouge2"][0]), np.array(PLAGES_HSV["rouge2"][1]))
mask_rouge = cv2.bitwise_or(mask_rouge1, mask_rouge2)
mask_bleu = cv2.inRange(hsv, np.array(PLAGES_HSV["bleu"][0]), np.array(PLAGES_HSV["bleu"][1]))

# Masque global pour la balise
masque_total = cv2.bitwise_or(mask_jaune, mask_rouge)
masque_total = cv2.bitwise_or(masque_total, mask_vert)
masque_total = cv2.bitwise_or(masque_total, mask_bleu)

# Nettoyage du masque (pour éliminer les petits bruits)
kernel = np.ones((5, 5), np.uint8)
masque_total = cv2.morphologyEx(masque_total, cv2.MORPH_OPEN, kernel)
masque_total = cv2.morphologyEx(masque_total, cv2.MORPH_CLOSE, kernel)

# Analyse de la position de la balise dans l'image (partition en 5 zones)
moments = cv2.moments(masque_total)
if moments["m00"] > 0:
    cx = int(moments["m10"] / moments["m00"])
    largeur = masque_total.shape[1]
    if cx < largeur * 0.2:
        position = "extrême gauche"
    elif cx < largeur * 0.4:
        position = "gauche"
    elif cx < largeur * 0.6:
        position = "centre"
    elif cx < largeur * 0.8:
        position = "droite"
    else:
        position = "extrême droite"
    print(f"La balise est dans la zone : {position} (x={cx}/{largeur})")

else:
    print("Balise non détectée")

