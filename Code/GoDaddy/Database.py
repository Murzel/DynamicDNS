from peewee import *

database = SqliteDatabase('Storage/GoDaddy.sqlite3', autoconnect=False)

class BaseModel(Model):
    class Meta:
        database = database
