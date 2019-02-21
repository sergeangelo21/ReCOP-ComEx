from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")

class AddMemberForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    middlename = StringField('Middle Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[("M","Male"),("F","Female")], validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    is_employed = RadioField(choices=[("Y","Yes"),("N","No")], validators=[DataRequired()])
    occupation = StringField('Occupation')
    income = StringField('Income')
    religion = StringField('Religion', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    telephone = StringField('Telephone')
    mobile = StringField('Mobile Number')
    submit = SubmitField('Add')

class ProposalForm(FlaskForm):
	category = SelectField('Category', coerce = int, validators=[DataRequired()])
	title = StringField('Title of the Activity', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])
	objective = StringField('Objective', validators=[DataRequired()])
	budget = StringField('Proposed Budget', validators=[DataRequired()])
	location = StringField('Venue', validators=[DataRequired()])
	event_date = StringField('Target Date', validators=[DataRequired()])
	submit = SubmitField('Submit')

class ProfilePersonalUpdateForm(FlaskForm):
    firstname = StringField('First Name')
    middlename = StringField('Middle Name')
    lastname = StringField('Last Name')
    gender = RadioField('Gender', choices=[("M","Male"),("F","Female")])
    birthday = DateField('Birthday')
    bio = StringField('Bio')
    submit = SubmitField('Update')

class ProfileContactUpdateForm(FlaskForm):
    address = StringField('Address')
    telephone = StringField('Telephone Number')
    mobile = StringField('Mobile Number')
    email = StringField('Email Address')
    submit = SubmitField('Update')

class ProfileUsernameUpdateForm(FlaskForm):
    username = StringField('Username')
    oldpassword = PasswordField('Old Password')
    submit = SubmitField('Update')

class PasswordUpdateForm(FlaskForm):
    oldpassword = PasswordField('Old Password')
    password = PasswordField('Password')
    submit = SubmitField('Update')

class ReferralForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Submit')