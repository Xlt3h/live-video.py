
import socket 
import utilis 
import pyautogui
import struct
import numpy as np 
import cv2
import pickle
class video_server:
    
    def server(self,host,port):
        self.host = host
        self.port = port
        self.s = socket.socket()
        self.s.bind((host,port))
        self.s.listen(10)
        self.conn, self.addr = self.s.accept()
    
    def live_vide(self):
        while True:
            try:
                self.record = pyautogui.screenshot()
                self.frame = np.array(self.record)
                #send the video via sockets using pickle
                self.v = pickle.dumps(self.frame)
                self.video_send = struct.pack("Q", len(self.v)) + self.v
                self.conn.sendall(self.video_send)
            except ConnectionResetError:
                print("connection was lost")
                #listen again for a new connection
                self.server(self.host,self.port)
    def client(self,host_c,port_c):
        self.host_c = host_c
        self.port_c = port_c
        self.s_c = socket.socket()
        self.s_c.connect((self.host_c,self.port_c))
        self.data = b""
        self.payload_size = struct.calcsize("Q")
        while True:
            while len(self.data) < self.payload_size:
                self.packet = self.s_c.recv(4*1024)
                if not self.packet: break
                self.data += self.packet
            self.packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            self.msg_size = struct.unpack("Q", self.packed_msg_size)[0]
            while len(self.data)<self.msg_size:
                self.data += self.s_c.recv(4*1024)
            self.frame_data = self.data[:self.msg_size]
            self.data = self.data[self.msg_size:]
            self.frame_ = pickle.loads(self.frame_data)
            cv2.imshow("Live",self.frame_)
            if cv2.waitKey(1) == ord('q'):
                break
        self.s_c.close()

    def record_video(self,filename):
        self.fps = 60.0
        self.filename = filename
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.resolution = (1920, 1080)
        self.out = cv2.VideoWriter(self.filename,self.codec,self.fps,self.resolution)
        while True:
            self.out.write(self.frame)
    
    def rec(self):
        import threading 
        thread_one = threading.Thread(target=self.record_video,args=(self.filename,))
        thread_one.start()

s = video_server()
t = str(input("Enter 1 for server and 2 for client: "))
if t == "1":
    s.server("127.0.0.1",4444)
    s.live_vide()
elif t == "2":
    s.client("127.0.0.1",4444)

