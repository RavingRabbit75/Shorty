from flask_wtf import FlaskForm
from wtforms import StringField, validators

class NewUser(FlaskForm):
	username = StringField("Username", [validators.Length(min=6)])


class EditUser(FlaskForm):
	username = StringField("Username", [validators.Length(min=6)])


class NewRedirect(FlaskForm):
	title = StringField("Title", [validators.Length(min=1)])
	url = StringField("URL", [validators.Length(min=1)])


class EditRedirect(FlaskForm):
	title = StringField("Title", [validators.Length(min=1)])
	url = StringField("URL", [validators.Length(min=1)])