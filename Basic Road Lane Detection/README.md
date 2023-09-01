# Merhaba arkadaşlar, video üzerinden basit bir şekilde şerit algılama uygulaması yapacağız.
Not : İçerikte kullanılan video repository içerisinde bulunan images-videos klasöründedir.
### 1. Kütüphanelerimizi dahil ederek başlayalım.

```
import cv2
import matplotlib.pyplot as plt
import numpy as np
```


### 2. Görüntülerimizi alalım.
```
cap = cv2.VideoCapture("roadVid1.mp4")

while cap.isOpened():
    ret, frame = cap.read()

    resizeImg = cv2.resize(frame, (960, 540))
    frame = cv2.resize(frame, (960, 540))
    # Bu iki satırda, aldığımız frameleri, daha düzgün çıktılar elde edebilmek için boyutlandırdık.

    if not ret:
        break

    cv2.imshow("Normal1", frame)

    if cv2.waitKey(300) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

Buradan alacağımız çıktı şu şekilde olacaktır:

<p align="center">
  <img width="960" height="540" src="https://github.com/burakOzden1/OpenCV-Projects/assets/133498595/55b74d3f-451c-4e95-9295-d64de8bc6371">
</p>

### 3. Fonksiyonlarımızı yazalım.
### 3.1 Canny kenar algılama fonksiyonumuz:
```
def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # alınan görseli gray hale getirdik
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 3)
    # görselimize blur uyguladık
    canny = cv2.Canny(blur, 70, 100)
    # gray hale gelmiş ve blurlanmış görselimiz üzerindeki kenarları tespit ettik
    return canny
```
Çıktımız:

<p align="center">
  <img width="960" height="540" src="https://github.com/burakOzden1/OpenCV-Projects/assets/133498595/1fd9a8a6-66b5-4e5e-aafc-c60b6ce65ae3">
</p>

### 3.2 Perspektifin uygulandığı fonksiyonumuz:

```
def perspektifArea(img):

    solAlt = (30, 520)
    solUst = (280, 390)
    sagUst = (680, 390)
    sagAlt = (930, 520)
    # Bu satırlarda perspektif uygulanacak penceremizin ölçülerini veriyoruz

    points = np.array([solAlt, solUst, sagUst, sagAlt], np.int32)
    points = points.reshape((-1, 1, 2))
    cv2.polylines(resizeImg, [points], isClosed=True, color=(0, 255, 204), thickness=3)
    # Burada ise ölçülerimize göre penceremizi çiziyoruz.

    pts1 = np.float32([solUst, solAlt, sagUst, sagAlt])
    pts2 = np.float32([[-30, -30], [-30, 570], [990, -30], [990, 570]])
    # Bu satırlarda ayrı bir pencere oluşturmak için belirli ölçüleri giriyoruz.

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformedFrame = cv2.warpPerspective(resizeImg, matrix, (960, 540))
    # Pencere ölçülerini alarak, değişkenlere atıyoruz.

    return transformedFrame
```
Çıktılarımız:

<p align="center">
  <img width="960" height="540" src="https://github.com/burakOzden1/OpenCV-Projects/assets/133498595/a69bb1f8-14f2-4b8f-8971-7df20e678632">
</p>
<p align="center">
  <img width="960" height="540" src="https://github.com/burakOzden1/OpenCV-Projects/assets/133498595/f7c53ef1-34ca-4db2-a2fd-29764aaee35d">
</p>

### 3.3 Algılanan çizgileri gösteren fonksiyonumuz:

```
def linesWrite(img):
    lines = cv2.HoughLinesP(canny(transformedFrame), 3, np.pi/180, 1)
    # HoughLinesP fonksiyonu yardımıyla, kenar fonksiyonu uyguladığımız penceremizde şeritlerimizin üzerini belirginleştiriyoruz.
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(transformedFrame, (x1, y1), (x2, y2), (98, 98, 239), 3)
    # Bu işlemi her frame için yapmamız gerekiyor, o yüzden for döngümüzden yararlanıyoruz.
    return transformedFrame
```
Çıktımız:

<p align="center">
  <img width="960" height="540" src="https://github.com/burakOzden1/OpenCV-Projects/assets/133498595/de626933-b05a-47d0-b13a-76739bf24d35">
</p>

## Kodlarımıza toplu bir şekilde bakalım:

```
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


cap = cv2.VideoCapture("roadVid1.mp4")

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

    if cv2.waitKey(300) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```
