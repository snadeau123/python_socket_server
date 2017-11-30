# Echo client program
import socket




class Client(object):

    def __init__(self):
        self.HOST = '52.229.33.101'  # The remote host
        #self.HOST = '127.0.0.1'
        self.PORT = 50007  # The same port as used by the server
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.data = self.s.recv(1024)
        print repr(self.data)

    def listen(self):
        while 1:
            self.data = self.s.recv(1024)
            if not self.data:
                break
            if self.data == 'q':
                break
            print repr(self.data)
        self.s.close()

if __name__ == '__main__':
    testclient = Client()
    testclient.listen()
