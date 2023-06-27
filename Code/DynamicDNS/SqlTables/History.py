from datetime import datetime

from DynamicDNS.Database import BaseModel
from peewee import *


class History(BaseModel):
    ip_address = TextField()
    timestamp = DateTimeField(default=datetime.now)
