from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User




#forms are all classes


# if we need to make a registration form
#vwe need to create a registation class

class RegistrationForm(FlaskForm):
    username =StringField('Username',
                            validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',
                            validators=[DataRequired(),Email()])
    password =PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password =PasswordField('Confirm Password',
                            validators=[DataRequired(),EqualTo('password')])
    submit =SubmitField('Sign Up')    
     
    #this is to check if the username already exists
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username already exists!')

    #this is to check if the email already exists
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists!')



class LoginForm(FlaskForm):
    
    email=StringField('Email',
                            validators=[DataRequired(),Email()])
    password =PasswordField('Password',
                            validators=[DataRequired()])
    remember =BooleanField('Remember Me')                        
    submit =SubmitField('Login')  



#now, when we login, we need to have an option to update our profile picture
#email or whatever we want
#the following for is for that purpose
#then import this form into route.py and could be used in the acount.html

class UpdateAccountForm(FlaskForm):
    username =StringField('Username',
                            validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',
                            validators=[DataRequired(),Email()])
    picture =FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit =SubmitField('Update')    
     
    #this is to check if the username and email are diff than the current username and email
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username already exists!')

    #this is to check the email simillarly
    def validate_email(self,email):
         if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email already exists!')




class RequestResetForm(FlaskForm):
    email=StringField('Email',
                            validators=[DataRequired(),Email()])
    submit =SubmitField('Request Password Reset') 
    # we need to check if the user has an account
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first')



class ResetPasswordForm(FlaskForm):
    password =PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password =PasswordField('Confirm Password',
                            validators=[DataRequired(),EqualTo('password')])
    submit =SubmitField('Reset Password')

#routes for both these forms are created