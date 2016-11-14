from flask_wtf import FlaskForm
from wtforms import StringField, validators

class NewUser(FlaskForm):
	# username = StringField("Username", 
	# 	[validators.Regexp("([A-Za-z0-9])\w+", message="Use only letters and numbers. No spaces.")], 
	# 	[validators.Length(min=6)])
	username = StringField("Username", [validators.Length(min=6)])

