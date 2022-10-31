

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db ,login_manager
from flask_login import UserMixin
from datetime import datetime
from flask import current_app

# a function with a decorator is created 
#this is for reloading the user from the UserID stored  
@login_manager.user_loader
def load_user(user_id):
    #now we can return the user for that ID 
    return User.query.get(int(user_id))
# now the extension will expect the user model to have certain attributes and methods
# like authenticator ( ie return true is proper credentials are provided.)
# and is active, is anonymous and get id - ALl these attributes could be inherited from 
# UserMixin
#the below User model has been inherited by adding UserMixin as attribute




# this model is to hold thedatabase

#creating user model 
#inheriting from db.model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #primary key coz, unique id for our user
    username =db.Column(db.String(20),unique=True, nullable=False)
    email =db.Column(db.String(120),unique=True, nullable=False)
    image_file =db.Column(db.String(20), nullable=False, default='default.jpg') # removed unique since they can have a default pic
    password= db.Column(db.String(60),nullable=False) #not unique, since people can have same passwords
    posts =db.relationship('Post' ,backref='author', lazy =True)
    
    
    #this is to reset password via email
    # we have imported serializer above
    # 1800 is 30 minutes 
    def get_reset_token(self, expires_sec=1800):
        #serializer object created, secret key is passed with expiation time
        s= Serializer(current_app.config['SECRET_KEY'],expires_sec)
        # and we can return a token created with this serializer
        #inside which we need to pass in a payload
        #which is the id of the user, which is decoded to utf 
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    #now we can put a method in place that can verify a token 
    #take in token as an argument
    @staticmethod
    def verify_reset_token(token):
        # there is a chance that the token could be invalid or the time could be expired
        #hence we use try except block
        s= Serializer(current_app.config['SECRET_KEY'])
        try:# first we try to get the user id
            user_id = s.loads(token)['user_id'] # 'user_id' is the payload we passed above
        except:
            return None
        # if we are able to get the user id without throwing an exception   
        #then we will return the user with the 
        return User.query.get(user_id)
    # we need 2 forms as well to complete this 


    
    
    
    
    
    #relationship that one user can make any number of posts, but each post has only
    #one author. Here, the post attribute has a relationship to the post model. 
    # back ref helps to get the user 
    #specifying a REPR method
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

#creating post class to hold the posts
#also inherits from db.model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    #we did not give datetime.utcnow() , but datetime.utcnow as we do not need the
    #time to e printed but the function is given as an argument
    content = db.Column(db.Text, nullable=False)
    #this is the id of the user who authored the post 
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable =False)
    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"


