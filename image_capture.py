import cv2
import numpy as np
# from datetime import datetime

def image_capture(folder_name = "cropped", ms_itv = 10000):
   '''
   INPUT
   folder_name : (str) The folder name which you want
   ms_itv : (int) Millisec time interval for capturing.

   '''
   video = cv2.VideoCapture(0)
   prev_time = int(round(time.time() * 1000)
   face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
   while True:
      cur_time = int(round(time.time() * 1000)
      check, img = video.read()
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

      faces = face_cascade.detectMultiScale(gray, 1.3, 5)
      for (x, y, w, h) in faces:
         cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
      cv2.imshow("CCTV", img)

      if cur_time - prev_time >= ms_itv:
         # Cropping face, distinguish different face, save it
         # Or save img, other process crop the face, and so on.
         prev_time = cur_time
         i = 0
         for (x, y, w, h) in faces:
            up = y - h / 2
            down = y + h / 2
            left = x - w / 2
            right = x + w / 2
            faceimg = img[up:down, left:right]
            cv2.imwrite("./" + folder_name + "/%d_%d.jpeg" %(cur_time, i), faceimg)
            i++
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break;

   video.release()
   cv2.destroyAllWindows()

if __name__ = "__main__":
   image_capture();

