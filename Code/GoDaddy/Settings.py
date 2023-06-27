from configparser import ConfigParser


class Settings:
    domain: str
    key: str
    secret: str

    def __init__(self):
        config = ConfigParser()
        config.read("Settings.conf")

        self.domain = config.get("GoDaddy", "domain")
        self.key = config.get("GoDaddy", "key")
        self.secret = config.get("GoDaddy", "secret")

    def getAuthorizationHeader(self):
        return {"Authorization": f"sso-key {self.key}:{self.secret}"}
        