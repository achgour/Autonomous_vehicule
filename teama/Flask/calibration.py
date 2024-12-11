import cv2
import time
import numpy as np


cap = cv2.VideoCapture(1)
images= []
patternSize = [9, 6]
while len(images) < 20:
    ret, frame = cap.read()
    if not ret:
        exit()
    cv2.imshow("tt",frame)
    res, _ = cv2.findChessboardCorners(frame, patternSize, None)
    if res:
        images.append(frame)
        time.sleep(2)

    if cv2.waitKey(1) & 0xFF == 27:
        exit()
    
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
pattern_size = (9, 6)  # Taille du motif (nombre de coins internes)

objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

objpoints = []  # Points 3D du monde réel
imgpoints = []  # Points 2D dans l'image

for img in images:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Recherchez les coins internes de l'échiquier
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

np.savez("calibration_params.npz", cameraMatrix=cameraMatrix, distCoeffs=distCoeffs)
print(cameraMatrix)
print(distCoeffs)