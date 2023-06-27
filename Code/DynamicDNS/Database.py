from peewee import *

database = SqliteDatabase('Storage/DynamicDNS.sqlite3', autoconnect=False)

class BaseModel(Model):
    class Meta:
        database = database
