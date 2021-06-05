from Code.DynDNS import DynDNS
from Code.GoDaddy import GoDaddy
from configparser import ConfigParser

config = ConfigParser()
config.read("Settings.conf")

if __name__ == "__main__":
    dyndns = DynDNS(config["DynDNS"]["username"], config["DynDNS"]["password"], int(config["DynDNS"]["port"]) if config["DynDNS"]["port"] else None)
    godaddy = GoDaddy(config["GoDaddy"]["domain"], config["GoDaddy"]["key"], config["GoDaddy"]["secret"])

    @dyndns.on_update
    def update(ip):
        if godaddy.getDNSRecord("A", "@").get("data") != ip:
            godaddy.updateDNSRecord("A", "@", ip)

    dyndns.run()