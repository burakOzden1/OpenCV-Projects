import cv2
import matplotlib.pyplot as plt
import numpy as np

def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 3)
    canny = cv2.Canny(blur, 70, 100)
    return canny

def linesWrite(img):
    lines = cv2.HoughLinesP(canny(transformedFrame), 3, np.pi/180, 1)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(transformedFrame, (x1, y1), (x2, y2), (98, 98, 239), 3)
    return transformedFrame

def perspektifArea(img):

    solAlt = (30, 520)
    solUst = (280, 390)
    sagUst = (680, 390)
    sagAlt = (930, 520)

    points = np.array([solAlt, solUst, sagUst, sagAlt], np.int32)
    points = points.reshape((-1, 1, 2))
    cv2.polylines(resizeImg, [points], isClosed=True, color=(0, 255, 204), thickness=3)

    pts1 = np.float32([solUst, solAlt, sagUst, sagAlt])
    pts2 = np.float32([[-30, -30], [-30, 570], [990, -30], [990, 570]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformedFrame = cv2.warpPerspective(resizeImg, matrix, (960, 540))

    return transformedFrame


cap = cv2.VideoCapture("roadVid9.mp4")

while cap.isOpened():
    ret, frame = cap.read()

    resizeImg = cv2.resize(frame, (960, 540))
    frame = cv2.resize(frame, (960, 540))

    if not ret:
        break

    cannyImg = canny(resizeImg)
    transformedFrame = perspektifArea(cannyImg)
    lines = linesWrite(transformedFrame)

    plt.imshow(canny(lines))

    cv2.imshow("Normal", resizeImg)
    cv2.imshow("Normal1", frame)
    cv2.imshow("Kenarlar", cannyImg)
    cv2.imshow("Transformed Frame", transformedFrame)
    cv2.imshow("Canny Transformed Frame", canny(transformedFrame))

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
