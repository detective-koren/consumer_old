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



def face_recog(target_face_path, input_face_path):
    
    '''
    INPUT
       - target_face_path (string) : full path to the target face
       - input_face_path (string)  : full path to the input face
    
    OUPUT
       - accuracy : the match rate between the target face and the input face.
                    the value is 1, when the target and the input is exactly match
                    the value is 0, when the target and the input is completely do NOT match
    '''
    
    target_face = face_recognition.load_image_file(target_face_path)
    input_face = face_recognition.load_image_file(input_face_path)
    
    target_encoding = face_recognition.face_encodings(target_face)
    input_encoding = face_recognition.face_encodings(input_face)

    face_distances = face_recognition.face_distance(target_encoding[0], input_encoding)
    
    accuracy = dist2accuracy(face_distances)
    
    print("target image {0} and input image {1} are {2:.2f}% match".format(target_face_path,
                                                                            input_face_path,
                                                                            accuracy*100))
    
    return accuracy
    
    
if __name__=='__main__':
    
    args = parser.parse_args()
    
    face_recog(args.target_face, args.input_face)
