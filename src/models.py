from . import db
from datetime import datetime

class Darckysources(db.Document):
    name     = db.StringField(unique=True, required=True, max_length=50, index=True)
    onion    = db.StringField(unique=True, required=True, max_length=128, index=True)
    type     = db.StringField(required=True, max_length=50, index=True)
    network  = db.StringField(required=True, max_length=50, index=True)
    caps     = db.ListField(db.ReferenceField("Capture"))
   
    def __repr__(self):
        """Define what is printed for the Darckysources object"""
        return f"Name: {self.name} id: {self.id}"


class Capture(db.Document):
    content      = db.StringField(required=True,  index=True)
    lenght       = db.StringField(Required=True, Index=True)
    date         = db.DateTimeField(default=datetime.utcnow, index=True)
    darky        = db.ReferenceField("Darckysources")

    def __repr__(self):
        """Define what is printed for the Capture object"""
        return f"date: {self.date} id: {self.id}"

class Email(db.Document):
    email    = db.StringField(unique=True, required=True, max_length=50, index=True)
    pwnd     = db.ListField(db.ReferenceField("PwnEmail"))

class PwnEmail(db.Document):
    up_date     = db.DateTimeField(default=datetime.utcnow, index=True)
    pwn_date    = db.StringField(required=True, max_length=50, index=True)
    breach      = db.StringField(required=True, max_length=50, index=True)
    email       = db.ReferenceField("Email")

class Phishing(db.Document):
    url         = db.StringField(unique=True, required=True, index=True)
    date         = db.DateTimeField(default=datetime.utcnow, index=True)
    