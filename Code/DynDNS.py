from Code.Socket_Helper import Server_Socket
from Code.Web_Response import HTTP_Response
from Code.Helper import *
import socket, re, base64, inspect, sqlite3

class DynDNS:
    current_ip = "UNKNOWN YET"
    __events = []
    logfile_filename = "DynDNS.log"


    def __init__(self, username : str, password : str, port : int = 1337) -> None:
        self.username = username
        self.password = password

        self.server = Server_Socket(port if port else 1337)

        # Connect to database, if not exist, create it
        self.logfile = sqlite3.connect("DynDNS.sqlite3")

        # Create table if not exist
        self.logfile.execute("""
            CREATE TABLE IF NOT EXISTS History(
                id INTEGER PRIMARY KEY, 
                ip TEXT NOT NULL,
                updated DATE DEFAULT CURRENT_TIMESTAMP
            );""")

        # Apply changes
        self.logfile.commit()

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
                                        print("New", self.addLog(ip))
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

    # logfile
    def addLog(self, ip : str) -> str:
        # Increment id by 1
        self.logfile.execute("""UPDATE History SET id = - (id + 1) WHERE id > 0;""")
        self.logfile.execute("""UPDATE History SET id = - id WHERE id < 0;""")

        # Add new entry
        self.logfile.execute(f"""INSERT INTO History(id, ip) VALUES(1, "{ip}");""")

        # Delete entries with id > 100
        self.logfile.execute("""DELETE FROM History WHERE id > 100""")
        
        # Apply changes
        self.logfile.commit()

        # Create text file with formatted output of tbl
        self.createLogfile()

        return f"Ip Adress {ip} has been logged"

    def createLogfile(self, entries : int = 100) -> None:
        with open(self.logfile_filename, "w") as f:
            f.write(self.logfileToString(entries))

    def logfileToString(self, entries : int = 100) -> str:
        stringBuilder = []

        stringBuilder.append("=" * 68)
        stringBuilder.append("{:^10}|{:^28}|{:^28}".format("Index", "IP Address", "Updated At"))
        stringBuilder.append("=" * 68)

        count = 0
        for entry in self.logfile.execute("SELECT * FROM History;").fetchall():
            stringBuilder.append("{:^10}|{:^28}|{:^28}".format(entry[0], entry[1], entry[2]))

            if (count := count + 1) >= entries:
                break

        return "\n".join(stringBuilder) + "\n"