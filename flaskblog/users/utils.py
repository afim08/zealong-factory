
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # remove the name of the file and add an 8 digit random hex
    #to avoid collition with existining name 
    #now using os module, we take the ention of the uploaded file to keep it as it is
    #this function returns both the name of file w/o extention and extension 
    #since we never use f_name ever, we can replace it with _ if needed 
    f_name,f_ext = os.path.splitext(form_picture.filename)
    #now combining the random hex with the file extension
    picture_fn = random_hex + f_ext
    #asking python where to save the file 
    #app.root.path gives fll path all the way upto package directory
    #join all these and file path is created by concatenation
    picture_path =os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    #we will resize the image
    output_size=(125,125)
    i =Image.open(form_picture)
    i.thumbnail(output_size)
    #the resized picture will be supplied 
    i.save(picture_path)
    #now we have saved the image into the db, but the user image is still the same default image
    #we need to update that . Hene we return the file here, 
    #and use the file below in the account form 
    return picture_fn


# we will create a function that can send email 
#pip install flask-mail
# import that extension in __init__.py as well 
#create ports, then initialize
# import the mail instances
def send_reset_email(user):
    #send the user an email with reset token 
    token = user.get_reset_token()
    #the mail should need url with reset token
    msg =Message('Password Reset Request',
                 sender= 'reply@zealong.co.nz', 
                 recipients=[user.email])
    # _exteral is used to get absolute url and not relative url. 
    # relative urls
    msg.body =f''' To reset your password, visit the following link: 
{url_for('reset_token',token=token, _external =True)}

If you did not make this request then simply ignore this email. 
'''
    mail.send(msg)