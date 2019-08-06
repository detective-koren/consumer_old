from PIL import Image
import numpy as np
import face_recognition

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--target_face', type=str)
parser.add_argument('--input_face', type=str)



def dist2accuracy(dist):
    L2_norm = np.linalg.norm(dist, axis=0, ord=2)
    accuracy = 1/(1+L2_norm)
    return accuracy



if __name__=='__main__':
    
    args = parser.parse_args()
    
    target_face = face_recognition.load_image_file(args.target_face)
    input_face = face_recognition.load_image_file(args.input_face)
    
    target_encoding = face_recognition.face_encodings(target_face)
    input_encoding = face_recognition.face_encodings(input_face)
    
    face_distances = face_recognition.face_distance([target_encoding], input_encoding[0])
    
    accuracy = dist2accuracy(face_distances[0])
    
    print("target image {0} and input image {1} are {2:.2f}% match".format(args.target_face,
                                                                            args.input_face,
                                                                            accuracy*100))
