from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, BooleanField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    middlename = StringField('Middle Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[("M","Male"),("F","Female")], validators=[DataRequired()])
    company = StringField('Company Name', validators=[DataRequired()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    telephone = StringField('Telephone', validators=[DataRequired()])
    mobile = StringField('Mobile Number', validators=[DataRequired()])
    sscr = RadioField('SSCR Member?', choices=[("Y","Yes"),("F","No")], validators= [DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Submit')