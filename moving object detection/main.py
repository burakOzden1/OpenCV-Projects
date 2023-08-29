import cv2

cap = cv2.VideoCapture("video1.mp4")

movingObjects = cv2.createBackgroundSubtractorMOG2()
# Hareketli nesneleri algılamaya yardımcı ilk maskemizi uyguladık

while True:
    ret, frame = cap.read()

    mask = movingObjects.apply(frame)

    cv2.imshow("Frame", frame)
    cv2.imshow("Moving", mask)

    keyCode = cv2.waitKey(10)

    if cv2.getWindowProperty("Frame", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
