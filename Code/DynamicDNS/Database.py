from peewee import *

db = SqliteDatabase('Storage/DynamicDNS.sqlite3', autoconnect=False)

class Database(Model):
    class Meta:
        database = db

class DBConnection:
    def __enter__(self) -> bool:
        return db.connect()
        
    def __exit__(self, exc_type, exc_value, exc_traceback) -> bool:
        return db.close()