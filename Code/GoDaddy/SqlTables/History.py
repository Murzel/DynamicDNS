from datetime import datetime

from GoDaddy.Database import Database
from peewee import *


class History(Database):
    type = TextField()
    name = TextField()
    ip_address = TextField()
    timestamp = DateTimeField(default=datetime.now)