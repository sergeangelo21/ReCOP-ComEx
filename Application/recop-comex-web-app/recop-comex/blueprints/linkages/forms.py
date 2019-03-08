from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, DecimalField, DateField, RadioField, IntegerField, MultipleFileField, HiddenField, validators
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, EqualTo, ValidationError, NumberRange, Email

class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")

class PictureForm(FlaskForm):
    photo = FileField("Photo", validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Invalid file!')])
    submit = SubmitField("Change Picture")
    
class PhotoForm(FlaskForm):
    photos   = MultipleFileField('Photos to Add', validators=[DataRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Invalid file!')])
    submit = SubmitField('Upload')

class CaptionForm(FlaskForm):
    photo = HiddenField('Photo', validators=[DataRequired()])
    caption = StringField('Caption', widget=TextArea())
    submit= SubmitField('Save')      

class ProposalForm(FlaskForm):
    title = StringField('Title of the Activity', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    objective = StringField('Objective', validators=[DataRequired()])
    budget = IntegerField('Estimated Budget', validators=[DataRequired()])
    location = StringField('Venue', validators=[DataRequired()])
    event_date = DateField('Target Date', validators=[DataRequired()])
    participant_no = IntegerField('No. of Participants', validators=[DataRequired()])
    min_age = IntegerField('Min Age', validators=[DataRequired()])
    max_age = IntegerField('Max Age', validators=[DataRequired()])
    thrust = SelectField('Thrust', choices = [("0","Please Choose One"),("1","Educational"),("2","Environmental"),("3","Health"),("4","Livelihood"),("5","Socio-Political"),("6","Spiritual")], validators=[DataRequired()])
    target_link = StringField('Target Linkages')
    select_link = SelectField('Select Linkages', choices=[("0", "Please Choose Here")])
    budget_plan = FileField('Budget Plan', validators=[FileRequired(), FileAllowed(['doc', 'docx'], 'Invalid file!')])
    programme = FileField('Programme', validators=[FileRequired(), FileAllowed(['doc', 'docx'], 'Invalid file!')])
    submit = SubmitField('Submit')

class AttachLetterForm(FlaskForm):
    attach_letter = FileField('Attach Letter', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Invalid file!')])
    event_id = StringField('Event ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EvaluationForm(FlaskForm):

    rating  = RadioField('Rating', choices=[('5','Five'),('4','Four'),('3','Three'),('2','Two'),('1','One')], validators=[DataRequired()])
    participant = StringField('Participant', validators=[DataRequired()])
    comment = StringField('Comment', widget=TextArea())
    submit= SubmitField('Submit')

class DonationForm(FlaskForm):
    give_to = RadioField('Give To', choices=[('1','Community'), ('2','Event')], validators=[DataRequired()])
    sponsee = SelectField('Communities', choices=[('','ReCOP')])
    event = SelectField('Events', choices=[('', 'Please Choose One')])
    type = RadioField('Donation Type', choices=[('1','Money'), ('2','In kind')], validators=[DataRequired()])
    amount = IntegerField('Amount')
    trans_slip   = FileField('Deposit Slip', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Invalid file!')])
    submit = SubmitField('Donate')

class ReferralForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    type = SelectField('Type', choices=[('', 'Please Choose One'), ('1', 'Volunteer'), ('2', 'Linkage'), ('3', 'Community')])
    submit = SubmitField('Submit')

class ProfilePersonalUpdateForm(FlaskForm):
    firstname = StringField('First Name', [validators.Length(min=0, max=30)])
    middlename = StringField('Middle Name', [validators.Length(min=0, max=20)])
    lastname = StringField('Last Name', [validators.Length(min=0, max=20)])
    gender = RadioField('Gender', choices=[("M","Male"),("F","Female")])
    birthday = DateField('Birthday')
    bio = StringField('Bio', [validators.Length(min=0, max=160)])
    submit = SubmitField('Update')

class ProfileContactUpdateForm(FlaskForm):
    address = StringField('Address', [validators.Length(min=0, max=100)])
    telephone = StringField('Telephone Number', [validators.Length(min=0, max=15)])
    mobile = StringField('Mobile Number', [validators.Length(min=0, max=25)])
    email = StringField('Email Address', [validators.Length(min=0, max=30)] )
    submit = SubmitField('Update')

class ProfileUsernameUpdateForm(FlaskForm):
    username = StringField('Username')
    oldpassword = PasswordField('Old Password')
    submit = SubmitField('Update')

class PasswordUpdateForm(FlaskForm):
    oldpassword = PasswordField('Old Password')
    password = PasswordField('Password', [validators.Length(min=0, max=60)] )
    submit = SubmitField('Update')