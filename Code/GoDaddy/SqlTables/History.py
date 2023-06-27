from datetime import datetime

from GoDaddy.Database import BaseModel
from peewee import *


class History(BaseModel):
    type = TextField()
    name = TextField()
    ip_address = TextField()
    timestamp = DateTimeField(default=datetime.now)
