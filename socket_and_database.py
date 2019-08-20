from socket import *
from influxdb import InfluxDBClient
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

"""
Tower sending part
It doesn't consider multiple client
We have to change socket to kafka? maybe
"""
def send_target(file_path):
    
    server_addr = ""
    server_port = 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_addr, server_port))
    server_socket.listen(1)
    sock, addr = server_socket.accept()
   
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    frame = cv2.imread(file_path)
    result, imgencode = cv2.imencode('.jpeg', frame, params = encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    #String 형태로 변환한 이미지를 socket을 통해서 전송
    sock.send( str(len(stringData)).ljust(16));
    sock.send( stringData );
    sock.close()
    
    """
    #다시 이미지로 디코딩해서 화면에 출력. 그리고 종료
    decimg=cv2.imdecode(data,1)
    cv2.imshow('CLIENT',decimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    """

def receive_and_store(server_addr, server_port, folder_name):

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_addr, server_port))

    recv_length = recvall(client_socket, 16)
    stringData = recvall(conn, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    client_socket.close()
    
    decimg=cv2.imdecode(data,1)
    cv2.imwrite(folder_name + file_name, decimg)

    json_body = [
        {
                "file_name": file_name,
                "target_id": target_id,
                "nuc_id": nuc_id
        }
    ]

    client = InfluxDBClinet('localhost', 8086, 'root', 'root', 'targets')
    # client.create_database('targets')
    client.write_points(json_body)
    # result = client.query("select value from file_name")
