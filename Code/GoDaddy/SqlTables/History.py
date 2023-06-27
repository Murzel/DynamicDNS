from datetime import datetime

from peewee import *

from Code.GoDaddy.Database import Database


class History(Database):
    type = TextField()
    name = TextField()
    ip_address = TextField()
    timestamp = DateTimeField(default=datetime.now)