# Merhaba arkadaşlar, video üzerinden basit bir şekilde şerit algılama uygulaması yapacağız.

### 1. Kütüphanelerimizi dahil ederek başlayalım.

```
import cv2
import matplotlib.pyplot as plt
import numpy as np
```


### 2. Görüntülerimizi alalım.
```
cap = cv2.VideoCapture("roadVid9.mp4")

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

### 3.2 Canny kenar algılama fonksiyonumuz:































