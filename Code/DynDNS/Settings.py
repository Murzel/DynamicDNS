from configparser import ConfigParser

class Settings:
    username: str
    password: str
    port: int

    def __init__(self):
        config = ConfigParser()
        config.read("Settings.conf")

        self.username = config.get("DynDNS", "username")
        self.password = config.get("DynDNS", "password")
        