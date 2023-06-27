import json

import requests

from Code.GoDaddy.Database import DBConnection
from Code.GoDaddy.SqlTables.History import History


class GoDaddy:
    base_url = "https://api.godaddy.com"
    
    def __init__(self, domain : str, key : str, secret : str) -> None:
        self.domain     = domain
        self.getHeaders = {"Authorization": "sso-key " + key + ":" + secret}
        self.putHeaders = self.getHeaders | {"Content-Type": "application/json"}

        with DBConnection():
            History.create_table()

    def toList(self, request : requests) -> dict:
        return json.loads(request.content.decode("utf-8"))[0]

    def getDNSRecord(self, type : str, name : str) -> dict: 
        return self.toList(requests.get(self.base_url + f"/v1/domains/{self.domain}/records/{type}/{name}", headers=self.getHeaders))

    def updateDNSRecord(self, type : str, name : str, ip : str):
        ttl = self.getDNSRecord("A", "@").get("ttl")
        body = json.dumps([{"data": ip, "name": name, "ttl": ttl, "type": type}])

        self.addLog(type, name, ip)

        return requests.put(self.base_url + f"/v1/domains/{self.domain}/records/{type}/{name}", body, headers=self.putHeaders).status_code

    def addLog(self, record_type : str, record_name : str,  record_ip : str) -> str:
        with DBConnection():
            History.create(type = record_type, name = record_name, ip_address = record_ip).\
                    save()
    
        print(f'GoDaddy DNS Record ({record_type}, {record_name}) updated to new ip ("{record_ip}")')