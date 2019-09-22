import cv2
import numpy as np
import time
# from datetime import datetime

def image_capture(folder_name = "cropped", ms_itv = 10000):
   '''
   INPUT
   folder_name : (str) The folder name which you want
   ms_itv : (int) Millisec time interval for capturing.

   '''
   video = cv2.VideoCapture(0)
   prev_time = int(round(time.time() * 1000))
   while True:
      cur_time = int(round(time.time() * 1000))
      check, img = video.read()
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
      cv2.imshow("CCTV", img)

      if cur_time - prev_time >= ms_itv:
         # Cropping face, distinguish different face, save it
         # Or save img, other process crop the face, and so on.
         prev_time = cur_time
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break;

   video.release()
   cv2.destroyAllWindows()

if __name__ == "__main__":
   image_capture();

