import cv2
import numpy as np

# Plages HSV des 4 couleurs de la balise
PLAGES_HSV = {
    "jaune": ((20, 100, 100), (35, 255, 255)),
    "vert":  ((40, 50, 50),   (85, 255, 255)),
    "rouge1": ((0, 100, 100), (10, 255, 255)),
    "rouge2": ((160, 100, 100), (180, 255, 255)),
    "bleu":  ((100, 100, 100), (130, 255, 255))
}

def generer_masque_balise(image_bgr):
    """Retourne un masque binaire où la balise colorée apparaît en blanc."""
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    masque_total = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for _, (bas, haut) in PLAGES_HSV.items():
        masque = cv2.inRange(hsv, np.array(bas), np.array(haut))
        masque_total = cv2.bitwise_or(masque_total, masque)

    # Nettoyage du masque
    kernel = np.ones((5, 5), np.uint8)
    masque_total = cv2.morphologyEx(masque_total, cv2.MORPH_OPEN, kernel)
    masque_total = cv2.morphologyEx(masque_total, cv2.MORPH_CLOSE, kernel)

    return masque_total

def position_balise_dans_image(masque):
    """Analyse le masque pour déterminer si la balise est à gauche, centre, droite ou absente."""
    moments = cv2.moments(masque)
    if moments["m00"] == 0:
        return None  # Aucune balise détectée

    cx = int(moments["m10"] / moments["m00"])
    largeur = masque.shape[1]

    if cx < largeur / 3:
        return "gauche"
    elif cx > 2 * largeur / 3:
        return "droite"
    else:
        return "centre"
