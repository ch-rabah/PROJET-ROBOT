import cv2
import numpy as np

IMAGE_PATH = "photo4.jpg"

def show_mask_with_detection():
    # 1) Lecture
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        raise FileNotFoundError(f"Impossible de lire « {IMAGE_PATH} »")
    h, w = img.shape[:2]

    # 2) Conversion HSV et masquage des 4 couleurs
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    plages = [
        ((20, 100, 100), (30, 255, 255)),   # jaune
        ((40,  50,  50), (80, 255, 255)),   # vert
        ((0,  100, 100), (10, 255, 255)),   # rouge1
        ((160,100, 100),(180,255,255)),     # rouge2
        ((100,100,100), (140,255,255)),     # bleu
    ]
    mask = np.zeros((h, w), dtype=np.uint8)
    for lo, hi in plages:
        mask |= cv2.inRange(hsv, np.array(lo), np.array(hi))

    # 3) Nettoyage morphologique
    ker = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, ker)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  ker)

    # 4) Recherche du plus grand contour
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv2.contourArea(c) > 0.005 * w * h]

    # Prépare l’image du mask pour y dessiner
    mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # 5) Si on trouve un contour valide, on dessine la bounding box
    if cnts:
        c = max(cnts, key=cv2.contourArea)
        x, y, wb, hb = cv2.boundingRect(c)
        cv2.rectangle(mask_bgr, (x, y), (x+wb, y+hb), (0, 255, 0), 2)

    # 6) Affichage
    cv2.imshow("Masque + détection de la balise", mask_bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    show_mask_with_detection()
