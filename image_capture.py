import cv2
import numpy as np
import time
import importlib
from os import listdir, remove
from os.path import isfile, join
from face_validation import face_recog
# from datetime import datetime

target = [f for f in listdir("./target") if isfile(join("./target", f))]

def image_capture(folder_name = "cropped", ms_itv = 100):
   '''
   INPUT
   folder_name : (str) The folder name which you want
   ms_itv : (int) Millisec time interval for capturing.

   '''
   video = cv2.VideoCapture(0)
   prev_time = int(round(time.time() * 1000))
   face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
   while True:
      cur_time = int(round(time.time() * 1000))
      check, img = video.read()
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      gray = cv2.equalizeHist(gray)

      faces = face_cascade.detectMultiScale(gray, 1.3, 5)
      for (x, y, w, h) in faces:
         img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)   
      cv2.imshow("CCTV1", img)

      if cur_time - prev_time >= ms_itv:
         # Cropping face, distinguish different face, save it
         # Or save img, other process crop the face, and so on.
         prev_time = cur_time
         i = 0
         
         for (x, y, w, h) in faces:
            faceimg = img[y:y + h, x:x + w]
            filename = "./" + folder_name + "/%d_%d.jpeg" %(cur_time, i)
            cv2.imwrite(filename, faceimg)
            i += 1
            for t in target:
               face_recog("./target/" + t, filename)
               remove(filename)
        
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break;

   video.release()
   cv2.destroyAllWindows()

if __name__ == "__main__":

   
   image_capture();

