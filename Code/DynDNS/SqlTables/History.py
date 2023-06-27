from datetime import datetime

from peewee import *

from Code.DynDNS.Database import Database


class History(Database):
    ip_address = TextField()
    timestamp = DateTimeField(default=datetime.now)