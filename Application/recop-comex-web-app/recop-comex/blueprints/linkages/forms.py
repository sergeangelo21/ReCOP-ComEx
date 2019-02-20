from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class ProposalForm(FlaskForm):
    title = StringField('Title of the Activity', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    objective = StringField('Objective', validators=[DataRequired()])
    budget = StringField('Estimated Budget', validators=[DataRequired()])
    location = StringField('Venue', validators=[DataRequired()])
    event_date = StringField('Target Date', validators=[DataRequired()])
    participant_no = StringField('No. of Participants', validators=[DataRequired()])
    min_age = StringField('Min Age', validators=[DataRequired()])
    max_age = StringField('Max Age', validators=[DataRequired()])
    thrust = SelectField('Thrust', choices = [("0","Please Choose One"),("1","Educational"),("2","Environmental"),("3","Health"),("4","Livelihood"),("5","Socio-Political"),("6","Spiritual")], validators=[DataRequired()])
    target_link = StringField('Target Linkages')
    select_link = SelectField('Select Linkages', choices=[("0", "Please Choose Here")])
    budget_plan = FileField('Budget Plan', validators=[FileRequired(), FileAllowed(['doc', 'docx'], 'Invalid file!')])
    programme = FileField('Programme', validators=[FileRequired(), FileAllowed(['doc', 'docx'], 'Invalid file!')])
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

class DonationForm(FlaskForm):
    give_to = RadioField('Give To', choices=[('1','Community'), ('2','Event')], validators=[DataRequired()])
    sponsee = SelectField('Communities', choices=[('','ReCOP')])
    event = SelectField('Events', choices=[('', 'Please Choose One')])
    type = RadioField('Donation Type', choices=[('1','Money'), ('2','In kind')], validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    trans_slip   = FileField('Deposit Slip', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Invalid file!')])
    submit = SubmitField('Donate')

class ReferralForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
