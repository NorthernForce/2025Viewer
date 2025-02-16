import sys
import time
from ultralytics import YOLO
import cv2

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} path/to/model.pt")
    sys.exit(1)

model = YOLO(sys.argv[1])

w, h = 640, 480
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, w)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
camera.set(cv2.CAP_PROP_FPS, 60)

fps = 0
while True:
    start = time.time()
    err, img = camera.read()
    if not err:
        print("error reading image, continuing")
        continue
    preds = model(img)
    for pred in preds:
        img = cv2.rectangle(img, )
    img = cv2.putText(img, f"fps: {fps:.0f}", (30, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("fun", img)
    cv2.waitKey(1) # currently shows image, needs python 3.10 for cscore library
    fps = 1 / (time.time() - start)