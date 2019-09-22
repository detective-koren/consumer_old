import cv2
import numpy as np
import time
import importlib
import face_recognition
from os import listdir, remove
from os.path import isfile, join
# from datetime import datetime

target = [f for f in listdir("./target") if isfile(join("./target", f))]

def image_capture(folder_name = "cropped", ms_itv = 100):
   '''
   INPUT
   folder_name : (str) The folder name which you want
   ms_itv : (int) Millisec time interval for capturing.

   '''
   video = cv2.VideoCapture(0)

   known_face_encodings = []
   known_face_names = []

   for f in listdir("./target"):
      target_image = face_recognition.load_image_file("./target/" + f)
      target_face_encoding = face_recognition.face_encodings(target_image)[0]
      known_face_encodings.append(target_face_encoding)
      known_face_names.append(f)

   prev_time = int(round(time.time() * 1000))
   
   while True:
      cur_time = int(round(time.time() * 1000))
      ret, frame = video.read()
      
      small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
      rgb_frame = small_frame[:, :, ::-1]

      face_locations = face_recognition.face_locations(rgb_frame)
      face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

      i = 1
      face_names = []

      for face_encoding in face_encodings:
          
          matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
          name = "Unknown"

          face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
          best_match_index = np.argmin(face_distances)
          if matches[best_match_index]:
              name = known_face_names[best_match_index]

          face_names.append(name)

      for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
         
         top *= 4
         right *= 4
         bottom *= 4
         left *= 4

         # Draw a box around the face
         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

         # Draw a label with a name below the face
         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
         font = cv2.FONT_HERSHEY_DUPLEX
         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
      
         if cur_time - prev_time >= ms_itv:
            faceimg = small_frame[top: top + (top + bottom) // 2, left: left + (left + right) // 2]
            filename = "./" + folder_name + "/%d_%d.jpeg" %(cur_time, i)
            cv2.imwrite(filename, faceimg)
            i += 1
        
      cv2.imshow("CCTV1", frame)
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break;

   video.release()
   cv2.destroyAllWindows()

if __name__ == "__main__":

   
   image_capture();

