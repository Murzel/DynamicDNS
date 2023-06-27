from peewee import *

db = SqliteDatabase('Storage/DynamicDNS.sqlite3')

class Database(Model):
    class Meta:
        database = db