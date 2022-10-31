from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email
#name of the blueprint is passed
users =Blueprint('users', __name__)



@users.route("/register",methods =['GET','POST'])  
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form =RegistrationForm()
    if form.validate_on_submit():
        #first we need to hash the password entered when submit is validated 
        hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #creating a new user now
        #we will pass in the hashed password and not the text password entered by the user
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        #add this user to make changes to our database
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!.','success') 
        # flash accepts second argument ie, category, here we gave it success. 
        # after the form is filled, will redirect to home page, or it will stay in form page itself
        #they can now login with the newely created account
        return redirect(url_for('users.login')) #this 'login' is the name of the function  
    return render_template('register.html',title='Register', form =form)

@users.route("/login",methods =['GET','POST'])  
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form =LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page =request.args.get('next')
            return redirect(next_page) if next_page else redirect (url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html',title='Login', form =form)


# when logged in, there should be a logout menu in the navbar 
@users.route("/logout")  
def logout():
    logout_user()
    return redirect(url_for('home'))
    # we need to see the logout link in the nav bar
    # which will be done in the layout.html file




#now we try to create an account route where we can see things we posted 
# when we log in 
# we also need a template account.html as well
#if none of the user is logged in, the /account link will
#will ask to login to access the page
#hence, login_required is imported and added as a decorator 
#login_view is give in init file as well 
@users.route("/account",methods =['GET','POST'])  #here we are allowing get and post requests
@login_required
def account():
    form = UpdateAccountForm() # an instance is created and passed into template below
    if form.validate_on_submit(): #adding a condition to see if our form is valid when submitted
        if form.picture.data: #ie if a pic is uploaded
            picture_file =save_picture(form.picture.data) #calling the function
            current_user.image_file =picture_file

        #if validated we can update the username and email
        current_user.username =form.username.data
        current_user.email =form.email.data
        #sqlalchemy makes this easy that we can simply change the value of current user variables and 
        #then commit those
        db.session.commit()
        flash ('Your account has been updated! ','success')  #  now we can give a flash message if their account has been updated
        return redirect(url_for('users.account'))#redirect to account page
    elif request.method =='GET':
        #this is so that as soon as we go to the account page, 
        # our form would already be populated with our account info
        form.username.data=current_user.username
        form.email.data=current_user.email

    #profile image in static folder > profile pic folder
    #image_file is already defined in the User Model
    image_file =url_for('static',filename='profile_pics/'+ current_user.image_file)
    #we will pass that image file into our account template
    return render_template('account.html',title='Account', image_file =image_file, form=form )
    #we can use this image_file as the source( ie src) in account.html file



#this route is such that on a post, we can click on the user 
#and it will take you to the user and the users posts alone

@users.route("/user/<string:username>")
def user_posts(username):
    page =request.args.get('page', 1 ,type =int) 
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page =page, per_page =5)
    return render_template('user_posts.html', posts=posts, user=user) 
# a specific template user_posts is created fpr this user as well 





#this route is for requesting for resetting the password
@users.route("/reset_password", methods =['GET','POST']) 
def reset_request():
    # now to make sure that they are logged out when they reset password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form =ResetPasswordForm()
    #we will check if the form are submitted and validated 
    if form.validate_on_submit():
        #at this point they have submitted an email to out form 
        #hence, we will grab the user for that email 
        #first() implies we need to get the first user with that email
        user = User.query.filter_by(email=form.email.data).first()
        # now when we have this user, we need to send them an email 
        # with a token, with which they can replace their password
        #using the function we created above
        send_reset_email(user)
        flash(' An email has been sent with instructins to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form) 
    # now we can create this template that we rendered here
# after the template is created (similar to login.html) 
# we need to create a route for actual password reset 


#here we accept a token as a parameter 
@users.route("/reset_password/<token>", methods =['GET','POST']) 
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    #now we try to verify the user from the token 
    #using the user verify we created in the model.py just now 
    # and pass in the token from the url
    user=User.verify_reset_token(token)
    # the verify_reset_token we created in the model.py will take in a token as an argument 
    # and if it is valid it will return user with that user_id 
    #which was the payload we passed into the initial token. 
    #if we do not get a user back here, that implies that the token is either invalid or expired
    if user is None:
        flash('That is an invalid or expired Token', 'warning')
        # and we will take back to reset request page
        return redirect(url_for('users.reset_request'))
    #now if we get back a user, we can give them a form to update the password
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #similar to code snipet in register (above)
        hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password= hashed_password
        db.session.commit()
        flash('Your password has been updated.','success') 
        return redirect(url_for('users.login')) 
    return  render_template('reset_token.html', title='Reset Password', form=form)
    # now we can create the reset_token.html template