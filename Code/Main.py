from DynamicDNS.DynamicDNS import dynamicdns as dyndns
from GoDaddy.GoDaddy import godaddy

if __name__ == "__main__":
    @dyndns.on_update
    def update(ip):
        godaddy.updateDNSRecord("A", "@", ip)

    dyndns.run("0.0.0.0", 6337)
