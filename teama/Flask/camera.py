import cv2
import numpy as np

# Initialisation de la capture vidéo à partir de la caméra indexée à 1 (peut nécessiter des ajustements)
cap = cv2.VideoCapture(0)

# Valeurs de calibration de la caméra
mtx = np.array([[1.42537600e+03, 0, 3.18862919e+02], [0, 1.42359494e+03, 3.18862919e+02], [0, 0, 1]])
dist = np.array([1.45409792e-01, -6.79102965e-01, 4.34185027e-04, 2.89675789e-03, -1.50278040e+00])

def drawMarker(img, corners, color=(0, 255, 0)):
    # Dessine les lignes autour du marqueur détecté
    corners = np.array([corners[0], corners[3]], dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [corners], True, color)

def findAruco(marker_size=6, draw=True):
    # Obtient le dictionnaire ArUco et initialise le détecteur ArUco
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    markerIds = None
    _ , img = cap.read()
    undistorted_img = cv2.undistort(img, mtx, dist)
    # Détecte les marqueurs ArUco dans l'image
    markerCorners, markerIds, _ = detector.detectMarkers(undistorted_img)

    if markerIds is not None and draw:
        corners = markerCorners[0][0]
        liste_aruco = []
        for i in range(len(markerIds)):
            # Points du marqueur ArUco dans l'espace 3D
            marker_points = np.array([[-marker_size/2, marker_size/2, 0],
                                      [marker_size/2, marker_size/2, 0],
                                      [marker_size/2, -marker_size/2, 0],
                                      [-marker_size/2, -marker_size/2, 0]], dtype=np.float32)

            # Estime la pose du marqueur en utilisant solvePnP
            _, rvec, tvec = cv2.solvePnP(marker_points, markerCorners[i], mtx, dist, False, cv2.SOLVEPNP_IPPE_SQUARE)

            # Calcule la distance en mètres
            distance = tvec[2][0]
            # Calcule l'angle avec la caméra en radians et convertit en degrés
            theta = np.degrees(np.arctan(tvec[0][0] / tvec[2][0]) + np.pi/2)
            # Calcule l'orientation du capteur en radians et convertit en degrés
            phi = np.degrees(rvec[2][0] + np.pi/2)

            # Ajoute les informations à la liste
            liste_aruco.append((distance, theta, phi, markerIds[i][0]))

        undistorted_corners = cv2.undistortPoints(corners, mtx, dist)

        # Affiche la distance et les angles
        print(f"On est à : {distance:.2f} cm du marker et {markerIds}.")
        print(f"Angle entre la camera et la cible: {theta:.2f} degrés.")
        print(f"Orientation du capteur est : {phi:.2f} degrés.")

        drawMarker(undistorted_img, undistorted_corners)
        return distance,theta,phi,tvec[0][0],markerIds[0][0]
    

    #if cv2.waitKey(1) == 113:  # Appuyez sur 'q' pour quitter
        #break
while True :
    _ , img = cap.read()
    findAruco(img)
    cv2.imshow("img", img)

cap.release()
cv2.destroyAllWindows()
    
<<<<<<< Updated upstream
findAruco()
=======
>>>>>>> Stashed changes
