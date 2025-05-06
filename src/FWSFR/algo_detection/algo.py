import cv2
import numpy as np

# Nom du fichier image à traiter
IMAGE_PATH = "photo5.jpg"  # À adapter selon ton image

# Plages HSV des 4 couleurs de la balise
PLAGES_HSV = {
    "jaune": ((20, 100, 100), (35, 255, 255)),
    "vert":  ((40, 50, 50),   (85, 255, 255)),
    "rouge1": ((0, 100, 100), (10, 255, 255)),
    "rouge2": ((160, 100, 100), (180, 255, 255)),
    "bleu":  ((100, 100, 100), (130, 255, 255))
}

def generer_masque_balise(image_bgr):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    masque_total = np.zeros(hsv.shape[:2], dtype=np.uint8)

    for nom, (bas, haut) in PLAGES_HSV.items():
        masque = cv2.inRange(hsv, np.array(bas), np.array(haut))
        masque_total = cv2.bitwise_or(masque_total, masque)

    # Nettoyage du masque
    kernel = np.ones((5, 5), np.uint8)
    masque_total = cv2.morphologyEx(masque_total, cv2.MORPH_OPEN, kernel)
    masque_total = cv2.morphologyEx(masque_total, cv2.MORPH_CLOSE, kernel)

    return masque_total

# Programme principal pour test
if __name__ == "__main__":
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print("Erreur : image non trouvée.")
        exit()

    masque = generer_masque_balise(image)

    # Affichage
    cv2.imwrite("masque_balise_final.png", masque)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
