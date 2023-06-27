from configparser import ConfigParser

from DynDNS.DynDNS import dyndns
from GoDaddy.GoDaddy import GoDaddy

config = ConfigParser()
config.read("Settings.conf")

if __name__ == "__main__":
    godaddy = GoDaddy(config["GoDaddy"]["domain"], config["GoDaddy"]["key"], config["GoDaddy"]["secret"])

    @dyndns.on_update
    def update(ip):
        godaddy.updateDNSRecord("A", "@", ip)

    dyndns.run("0.0.0.0", 6337)