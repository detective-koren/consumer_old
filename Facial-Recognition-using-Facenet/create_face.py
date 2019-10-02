import cv2
import numpy as np
import os, time
import imutils
from imutils.video import VideoStream

FACE_DIR = "incept/"

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def main():
    
    name=input("EnterName: ")
    face_id = int(input("Enter id for face: "))
    
    create_folder(FACE_DIR)
    face_folder = FACE_DIR + str(face_id) + "/"
    create_folder(face_folder)

    img_no = 1
    total_imgs = 10

    vs = VideoStream(src=0).start()

    net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
    
    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        width, height = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 177, 123])
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x1, y1, x2, y2) = box.astype("int")

                face_img = frame[y1:y2, x1:x2]
                img_path = face_folder + name + str(img_no) + ".jpg"
                cv2.imwrite(img_path, face_img)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.imshow("Saving", face_img)
                img_no += 1

        cv2.imshow("CCTV", frame)
        key = cv2.waitKey(1) & 0xFF

        if (key == ord("q")):
            break

        if img_no == total_imgs:
            break

    cv2.destroyAllWindows()
    vs.stop()

main()
