'''
created by ritshidze nemudzivhadi
github xlt3h
'''

import socket  
import cv2

class video_server:
    
    def server(self,host,port):
        self.host = host
        self.port = port
        self.s = socket.socket()
        self.s.bind((host,port))
        self.s.listen(1) #listen to one connection
        self.conn, self.addr = self.s.accept()
    
    def server_recv_video(self):
        while True:
            try:
                self.data = self.conn.recv(2048000)
                self.img = open("img.jpg","wb")
                if self.data:
                    self.img.write(self.data)
                    self.img = cv2.imread("img.jpg")
                    cv2.imshow("img",self.img)
                    if cv2.waitKey(1) == ord('q'):
                        break
                else:
                    print("client connection closed")
                    break
            except :
                print("an error occured")
                print("restarting the server")
                #listen again for a new connection
                self.server(self.host,self.port)
        #close everything
        cv2.destroyAllWindows()
        self.s.close()
        self.conn.close()
        #end of server

    def client(self,host_c,port_c):
        try:
            self.host_c = host_c
            self.port_c = port_c
            self.s_c = socket.socket()
            self.s_c.connect((self.host_c,self.port_c))
            self.cap =cv2.VideoCapture(0)
            while True:
                self.ret , self.photo= self.cap.read()

                cv2.imwrite("img_1.jpg",self.photo)
                self.file = open("img_1.jpg","rb")
                self.img_data = self.file.read(2048000)
                self.s_c.send(self.img_data)            
                if cv2.waitKey(1) == ord('q'):
                    break
        except:
            print("an error occured reconnecting...")
            self.client(self.host_c,self.port_c)
        self.s_c.close()
        self.cap.release()
        cv2.destroyAllWindows()
        self.file.close()
        #end of client

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
    s.server_recv_video()
   
elif t == "2":
    s.client("127.0.0.1",4444)

