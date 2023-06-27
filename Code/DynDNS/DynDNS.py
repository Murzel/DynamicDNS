import inspect

from DynDNS.Database import DBConnection
from DynDNS.Settings import Settings
from DynDNS.SqlTables.History import History
from flask import Flask, request


class DynDNS(Flask):
    settings: Settings = Settings()
    __current_ip: str = None
    __events = []
        
    @property
    def current_ip(self) -> str:
        return self.__current_ip

    @current_ip.setter
    def current_ip(self, ip):
        if not ip or self.__current_ip == ip: return

        self.__current_ip = ip

        with DBConnection():
            History.create(ip_address = ip).\
                    save()
        
        print(f"New Dynamic DNS Ip Address {ip} has been assigned")

        for event in self.__events:
            if len(inspect.signature(event).parameters.keys()) > 0:
                event(ip)
            else:
                event()

    def on_update(self, func):
        """
        A function decorated by that, will be triggered when the current_ip address changes 

        [0] : str = new current_ip address 
        """
        if callable(func):
            self.__events.append(func)
            return func

        return None

dyndns = DynDNS(__name__)

with DBConnection():
    History.create_table()

@dyndns.route("/", methods=["GET"])
def root():
    """ Returns current ip address"""
    if dyndns.current_ip:
        return (dyndns.current_ip, 200)
    
    return ("", 204) # No Content

@dyndns.route("/nic/update", methods=["GET"])
def update():
    if not request.authorization: return ("", 200)
    if request.authorization.username != dyndns.settings.username: return ("", 200)
    if request.authorization.password != dyndns.settings.password: return ("", 200)

    dyndns.current_ip = request.args.get("myip")

    return ("", 200)
