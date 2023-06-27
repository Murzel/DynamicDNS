from peewee import *

db = SqliteDatabase('Storage/GoDaddy.sqlite3')

class Database(Model):
    class Meta:
        database = db