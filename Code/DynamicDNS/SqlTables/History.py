from datetime import datetime

from DynamicDNS.Database import Database
from peewee import *


class History(Database):
    ip_address = TextField()
    timestamp = DateTimeField(default=datetime.now)