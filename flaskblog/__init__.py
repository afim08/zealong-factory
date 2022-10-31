from distutils.log import debug
from enum import unique
from turtle import title
import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # for password and its decryption
from flask_login import LoginManager # 'pip install flask-login' done for login 
from flask_mail import Mail # pip install flask-mail done before importing 
from flaskblog.config import Config


#render template helps to fetch htmmls templates made


#now creating a dataase instance
# The bes thing about sql alchemy is the the database structures could be used 
# as classes, and these classes be called as models.
db =SQLAlchemy()

bcrypt =Bcrypt()

#creating an instance of the login manager 
login_manager =LoginManager()
login_manager.login_view ='users.login' #'login' is the function name of our route
login_manager.login_message_category ='info' 


mail=Mail() # initailize extension


 
# now we can move the creation of our app into a function
# the reason being that it will allow us to create diff instances of our app with diff configurations
# here we create a function create_app and take arugument of our configuraion object

def create_app(config_class=Config):
    app = Flask(__name__) 
    # the __name__ will help help flask to look for templates and static files 
    # creating an instance of config from config.py file
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    from flaskblog.users.routes import users #importing the blueprint instances
    from flaskblog.posts.routes import posts #importing the blueprint instances
    from flaskblog.main.routes import main #importing the blueprint instances
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)   #registering the blueprint
    app.register_blueprint(posts) 
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app