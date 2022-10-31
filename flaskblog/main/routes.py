from flask import render_template, request, Blueprint
from flaskblog.models import Post

#name of the blueprint is passed
main =Blueprint('main',__name__)



# routes are what we type into browser to go to different pages. 
# route page of the website ie, home
# we can return html here, but we can return some textx as well
# we can add  more decorators that points to the same page
@main.route("/")  
@main.route("/home")
def home():
    #there is a post route below. 
    #Post.query.all be grad all those posts from the database
    #to grab the page we want , 1 in the argument is default page
    #type is given as int, so that it gives error if someone passes other than int
    page =request.args.get('page', 1 ,type =int)
    #posts = Post.query.all(), this will give all the posts, but we paginate using the code below
    #we will also pass the page into our query as page=page
    #order_by helps to sort by date updated 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page =page, per_page =5)
    return render_template('home.html', posts=posts) # posts argument = posts list 
    # argument is used in the home.html page

@main.route("/about")  
def about():
    return render_template('about.html')