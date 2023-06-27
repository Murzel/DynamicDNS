from datetime import datetime

from DynamicDNS.Database import BaseModel, database
from peewee import *


class History(BaseModel):
    ip_address = TextField()
    timestamp = DateTimeField(default=datetime.now)


with database:
    History.create_table()
