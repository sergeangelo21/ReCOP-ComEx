from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class ProposalForm(FlaskForm):
	category = SelectField('Category', coerce = int, validators=[DataRequired()])
	title = StringField('Title of the Activity', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	objective = StringField('Objective', validators=[DataRequired()])
	budget = StringField('Proposed Budget', validators=[DataRequired()])
	location = StringField('Venue', validators=[DataRequired()])
	event_date = StringField('Target Date', validators=[DataRequired()])
	submit = SubmitField('Submit')


class ProfileUpdateForm(FlaskForm):
    firstname = StringField('First Name')
    middlename = StringField('Middle Name')
    lastname = StringField('Last Name')
    gender = RadioField('Gender', choices=[("M","Male"),("F","Female")])
    birthday = DateField('Birthday')
    bio = StringField('Bio')
    company = StringField('Company Name')    
    address = StringField('Address')
    telephone = StringField('Telephone')
    mobile = StringField('Mobile Number')
    email = StringField('Email Address')
    username = StringField('Username')
    submit = SubmitField('Update')

class PasswordUpdateForm(FlaskForm):
    oldpassword = PasswordField('Old Password')
    password = PasswordField('Password')
    submit = SubmitField('Update')