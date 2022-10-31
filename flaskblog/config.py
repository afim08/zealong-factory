
import os
#the below secret key, db details could be given secretely using environment variables
#taught in Corey Schafer video number 11, 27 minutes onwards

class Config:
    SECRET_KEY = 'abcdef123456'
    #setting up the database location
    #a site.db will be created along with our py file in the directory 
    #we have setup the location here
    #SQLALCHEMY_DATABASE_URI ='sqlite:///site.db'
    DATABASE_URL ='postgres://ljruexzzfzetkc:bf2518d1bff71ec984fd0a109be6710d525ed991f9b81d2b8cd94371aa50a228@ec2-44-209-57-4.compute-1.amazonaws.com:5432/d4tkhtv4nqiu1j'
    #postgres://ljruexzzfzetkc:bf2518d1bff71ec984fd0a109be6710d525ed991f9b81d2b8cd94371aa50a228@ec2-44-209-57-4.compute-1.amazonaws.com:5432/d4tkhtv4nqiu1j


    #we need a mail server, mail port , TLS, username and password
    #setting up config variable
    #google mail is used here 
    MAIL_SERVER ='smtp.googlemail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS =True
    MAIL_USERNAME =os.environ.get('EMAIL_USER')
    MAIL_PASSWORD =os.environ.get('EMAIL_PASS')
   