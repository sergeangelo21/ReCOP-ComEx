from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, BooleanField, RadioField, IntegerField, validators
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email


class ReferralForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    type = SelectField('Type', choices=[('', 'Please Choose One'), ('1', 'Volunteer'), ('2', 'Linkage'), ('3', 'Community')])
    submit = SubmitField('Submit')
    
class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")
    
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
    bio = StringField('Bio', [validators.Length(min=0, max=160)])
    birthday = DateField('Birthday', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    telephone = StringField('Telephone Number')
    mobile = StringField('Mobile Number', [validators.Length(min=0, max=25)])
    sscr = RadioField('SSCR Member?', choices=[("Y","Yes"),("F","No")])
    type = StringField('Type', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    thrust = SelectField('Thrust', choices = [("0","Please Choose One"),("1","Education"),("2","Environmental"),("3","Health"),("4","Livelihood"),("5","Socio-Political"),("6","Spiritual")])
    submit = SubmitField('Submit')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
    email = StringField('Email Address', validators=[DataRequired()])
    type = SelectField('Type', choices=[('', 'Please Choose One'), ('1', 'Volunteer'), ('2', 'Linkage'), ('3', 'Community')])
    submit = SubmitField('Submit')
