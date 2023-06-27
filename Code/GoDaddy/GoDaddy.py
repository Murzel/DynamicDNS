import json

import requests
from GoDaddy.Database import database
from GoDaddy.Settings import Settings
from GoDaddy.SqlTables.History import History


class GoDaddy:
    base_url = "https://api.godaddy.com"
    settings = Settings()

    def __init__(self) -> None:
        with database:
            History.create_table()

    def toList(self, request : requests) -> dict:
        return json.loads(request.content.decode("utf-8"))[0]

    def getDNSRecord(self, type : str, name : str) -> dict: 
        return self.toList(requests.get(self.base_url + f"/v1/domains/{self.settings.domain}/records/{type}/{name}", headers=self.settings.getAuthorizationHeader()))

    def updateDNSRecord(self, type : str, name : str, ip : str):
        previous_record = self.getDNSRecord(type, name)
        
        # Check if an update is necessary
        if previous_record.get("data") == ip: 
            return

        # Assumes everything will be fine in the following put request...    
        print(f'GoDaddy DNS Record ({type}, {name}) updated to new ip ("{ip}")')

        with database:
            History.create(type = type, name = name, ip_address = ip).\
                    save()

        # Send actual request to update the ip address
        headers = self.settings.getAuthorizationHeader() | {"Content-Type": "application/json"}
        body = json.dumps([{"data": ip, "name": name, "ttl": previous_record.get("ttl"), "type": type}])

        return requests.put(self.base_url + f"/v1/domains/{self.settings.domain}/records/{type}/{name}", body, headers=headers).status_code
    
godaddy = GoDaddy()
