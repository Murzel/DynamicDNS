import base64
import inspect
import re
import socket

from Code.DynDNS.Database import DBConnection
from Code.DynDNS.SqlTables.History import History
from Code.Helper import *
from Code.Socket_Helper import Server_Socket
from Code.Web_Response import HTTP_Response


class DynDNS:
    current_ip = "UNKNOWN YET"
    __events = []

    def __init__(self, username : str, password : str, port : int = 1337) -> None:
        self.username = username
        self.password = password

        self.server = Server_Socket(port if port else 1337)

        with DBConnection():
            History.create_table()

    def run(self):
        # Magic / Logic - Depends on the view
        while True:
            try:
                client_socket, addr = self.server.accept()
                client_socket.settimeout(10.0)

                # print(HTTP_Response().get("200 OK", "Hallo Welt", "text/html;UTF-8").encode())
                message = client_socket.recv(4).decode()

                if message == "GET ":
                    while True:
                        message = client_socket.recv(1024).decode()
                        if message[len(message) - 4:] == "\r\n\r\n":
                            break

                    message = message.replace("\r\n", "\n")
                    firstline = re.search("\n", message)

                    requested    = msg[:pos] if (pos := (msg := message[:firstline.start()][:re.search(" ", message[:firstline.start()]).start()]).find("?")) > -1 else msg
                    HTTPVersion  = message[:firstline.start()].split()[-1]
                    getVariables = listToDict("=", msg[pos+1:].split("&")) if (pos := msg.find("?")) > -1 else None
                    message      = listToDict(":", list(map(str.strip, message[firstline.end():-2].split("\n"))))

                    if requested == "/":
                        with open("Code/Webserver/index.html", "r") as f:
                            html = f.read().replace("$ip", self.current_ip)

                        client_socket.sendall(HTTP_Response().MIME_text_html(html))
                    if requested == "/favicon.ico":
                        client_socket.sendall(HTTP_Response().MIME_image_favicon("Code/Webserver/favicon.ico"))
                    if requested == "/src/images/logo.png":
                        client_socket.sendall(HTTP_Response().MIME_image_png("Code/Webserver/src/images/logo.png"))
                    if requested == "/nic/update":
                        if getVariables:
                            if (ip := find_ip(getVariables.get("myip"))) and (credentials := message.get("Authorization")):
                                credentials = base64.b64decode(credentials.split()[1]).decode().split(":")
                                if self.username == credentials[0] and self.password == credentials[1]:
                                    if self.current_ip != ip:
                                        self.current_ip = ip
                                        self.__trigger_update()
                                        self.addLog(ip)

                                        client_socket.sendall(HTTP_Response().STATUS_no_content())
                    else:
                        # client_socket.sendall(HTTP_Response().MIME_text_html("Page not found - 404"))
                        client_socket.sendall(HTTP_Response().STATUS_not_found())

                client_socket.shutdown(socket.SHUT_RDWR)
                client_socket.close()
            
            except Exception as e:
                pass

    # Event Handling
    def on_update(self, func):
        """
        A function decorated by that, will be triggered when the public ip address changes 

        [0] : str = New IP Address 
        """
        if callable(func):
            self.__events.append(func)
            return func

        return None

    def __trigger_update(self):
        for event in self.__events:
            if len(inspect.signature(event).parameters.keys()) > 0:
                event(self.current_ip)
            else:
                event()

    def addLog(self, ip : str) -> str:
        with DBConnection():
            History.create(ip_address = ip).\
                    save()
        
        print(f"New Dynamic DNS Ip Address {ip} has been assigned")