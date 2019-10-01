import cv2
import numpy as np
import time
import importlib
import face_recognition
from os import listdir, remove
from os.path import isfile, join
# from datetime import datetime

known_face_encodings = []
known_face_names = []

def collect_target():
   for f in listdir("./target"):
      target_image = face_recognition.load_image_file("./target/" + f)
      target_face_encoding = face_recognition.face_encodings(target_image)[0]
      known_face_encodings.append(target_face_encoding)
      known_face_names.append(f)

def consume_and_find(folder_name = "cropped", ms_itv = 100):
   '''
   INPUT
   folder_name : (str) The folder name which you want
   ms_itv : (int) Millisec time interval for capturing.

   '''
   # TODO
   # Implement a consumer part of kafka
   # Let the image file be 'frame'
   # and the face locations be 'face_locations'

   refactor = [1, 0.5, 0.25]
   resize_idx = 2
   cur_time = int(round(time.time() * 1000))

   small_frame = cv2.resize(frame, (0, 0), fx=refactor[resize_idx], fy=refactor[resize_idx])
   rgb_frame = small_frame[:, :, ::-1]

   face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

   i = 1
   face_names = []

   for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
      face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
      best_match_index = np.argmin(face_distances)

      if matches[best_match_index]:
         name = known_face_names[best_match_index]
         face_names.append(name)

         top *= 1 // y_refactor[resize_idx]
         right *= 1 // x_refactor[resize_idx]
         bottom *= 1 // y_refactor[resize_idx]
         left *= 1 // x_refactor[resize_idx]

         faceimg = small_frame[top: top + (top + bottom) // 2, left: left + (left + right) // 2]
         filename = "./" + folder_name + "/%d_%d.jpeg" %(cur_time, i)
         cv2.imwrite(filename, faceimg)
         i += 1

if __name__ == "__main__":

   collect_target()

   while True:
      consume_and_find()
