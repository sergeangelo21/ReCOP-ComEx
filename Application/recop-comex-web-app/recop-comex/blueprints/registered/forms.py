from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, BooleanField, RadioField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class DonationForm(FlaskForm):

    give_to = RadioField('Give To', choices=[(1,'Community'), (2,'Event')])
    sponsee = SelectField('Communities', choices=[('1','ReCOP')], coerce=int)
    event = SelectField('Events', choices=[('0', 'Please Choose One')], coerce=int)
    type = RadioField('Donation Type', choices=[('1','Money'), ('2','In kind')])
    amount = StringField('Amount', validators=[DataRequired()])
    trans_slip   = FileField('Deposit Slip', validators=[DataRequired()])
    submit = SubmitField('Donate')

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