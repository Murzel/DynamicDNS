import socket

class Server_Socket():
    __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, port):
        self.__ip   = "0.0.0.0" # allowing connections only from local network
        self.__port = port
        self.name = "Server"

        self.sock.bind((self.ip, self.port))
        self.sock.listen()

        print("Server starts running at port", self.port)
    
    @property
    def sock(self):
        return self.__sock

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    def accept(self):
        return self.sock.accept()

    def __del__(self):
        self.sock.close()