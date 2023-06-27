# DynamicDNS

This project keeps track of your public ip address by listening to your router (DynV2 protocol).

It's very easy to trigger your own code by defining a decorated function.
An example, where the GoDaddy DNS Record will be updated, is already provided in the code.

Requirements:
- Python 3.9
- Sqlite3

Required Python libraries:
- Flask (Webserver)
- peewee (SQL-ORM)
