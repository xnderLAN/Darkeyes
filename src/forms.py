from unicodedata import name
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField

class DarkysForm(Form):
    name   = StringField("name", [validators.length(min=2, max=25)])
    onion  = StringField("url", [validators.length(min=10, max=200)])
    type   = IntegerField("type", [validators.NumberRange(min=0, max=2)])
    network= IntegerField("network", [validators.NumberRange(min=0, max=1)])

