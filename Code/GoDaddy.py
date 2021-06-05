import requests, json, sqlite3

class GoDaddy:
    base_url     = "https://api.godaddy.com"
    log_filename = "GoDaddy.log"
    
    def __init__(self, domain : str, key : str, secret : str) -> None:
        self.domain     = domain
        self.getHeaders = {"Authorization": "sso-key " + key + ":" + secret}
        self.putHeaders = self.getHeaders | {"Content-Type": "application/json"}

        # Connect to database, if not exist, create it
        self.DynDNS = sqlite3.connect("DynDNS.sqlite3")

        # Create table if not exist
        self.DynDNS.execute("""
            CREATE TABLE IF NOT EXISTS GoDaddy(
                id INTEGER PRIMARY KEY, 
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                ip TEXT NOT NULL,
                updated DATE DEFAULT CURRENT_TIMESTAMP
            );""")

        # Apply changes
        self.DynDNS.commit()


    def toList(self, request : requests) -> dict:
        return json.loads(request.content.decode("utf-8"))[0]

    def getDNSRecord(self, type : str, name : str) -> dict: 
        return self.toList(requests.get(self.base_url + f"/v1/domains/{self.domain}/records/{type}/{name}", headers=self.getHeaders))

    def updateDNSRecord(self, type : str, name : str, ip : str):
        ttl = self.getDNSRecord("A", "@").get("ttl")
        body = json.dumps([{"data": ip, "name": name, "ttl": ttl, "type": type}])

        print(self.addLog(type, name, ip))

        return requests.put(self.base_url + f"/v1/domains/{self.domain}/records/{type}/{name}", body, headers=self.putHeaders).status_code


    def addLog(self, record_type : str, record_name : str,  record_ip : str) -> str:
        # Increment id by 1
        self.DynDNS.execute("""UPDATE GoDaddy SET id = - (id + 1) WHERE id > 0;""")
        self.DynDNS.execute("""UPDATE GoDaddy SET id = - id WHERE id < 0;""")

        # Add new entry
        self.DynDNS.execute(f"""INSERT INTO GoDaddy(id, type, name, ip) VALUES(1, "{record_type}", "{record_name}", "{record_ip}");""")

        # Delete entries with id > 100
        self.DynDNS.execute("""DELETE FROM GoDaddy WHERE id > 100""")
        
        # Apply changes
        self.DynDNS.commit()

        self.createLogFile()

        return f'DNS Record ({record_type}, {record_name}) updated to new ip ("{record_ip}") at {self.DynDNS.execute("""SELECT updated FROM GoDaddy WHERE id = 1""").fetchone()[0]}'

    def createLogFile(self, entries : int = 100) -> None:
        with open(self.log_filename, "w") as f:
            f.write(self.logFileToString(entries))

    def logFileToString(self, entries : int = 100) -> str:
        stringBuilder = []

        stringBuilder.append("=" * 126)
        stringBuilder.append("{:^10}|{:^28}|{:^28}|{:^28}|{:^28}".format("Index", "Type", "Name", "IP Address", "Updated At"))
        stringBuilder.append("=" * 126)

        count = 0
        for entry in self.DynDNS.execute("SELECT * FROM GoDaddy;").fetchall():
            stringBuilder.append("{:^10}|{:^28}|{:^28}|{:^28}|{:^28}".format(entry[0], entry[1], entry[2], entry[3], entry[4]))

            if (count := count + 1) >= entries:
                break

        return "\n".join(stringBuilder) + "\n"