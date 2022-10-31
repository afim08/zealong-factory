from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

#name of the blueprint is passed
posts =Blueprint('posts',__name__)



# route for a new post
@posts.route("/post/new", methods =['GET','POST']) 
@login_required #creating a new post requires a user to be logged in 
def new_post():
    form =PostForm()
    if form.validate_on_submit():
        #create post
        post =Post(title=form.title.data, content=form.content.data, author=current_user)
        #add the post to db
        db.session.add(post)
        db.session.commit()
        #a flash message showing that a post has been created and then redirect them 
        #back to the homepage
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form, legend ='New Post')
    


#there should be an option to update or delete the posts
# a route need to be created to take us to a specific page that contains a single post
# if the user goes to post/1, then post_id =1 and so on 
#and we want that to be an integer
@posts.route("/post/<int:post_id>")
def post(post_id):
    #now within the route lets fetch the post if it exists
    #get_or_404 implies, get the post if it exists if not return 404 error
    post =Post.query.get_or_404(post_id)
    return render_template('post.html',title =post.title, post =post)
    #now create a template named post.html in template folder


# a route to update and delete a post 
@posts.route("/post/<int:post_id>/update", methods =['GET','POST'])
@login_required #login is required to update as we only need a user to update a post
def update_post(post_id):
    post =Post.query.get_or_404(post_id)
    #now we need to make it in a way that only the person who wrote the post can update it 
    if post.author != current_user:
        abort(403)
        #now we need to create a form and render a template
    form =PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated.')
        return redirect(url_for('posts.post',post_id=post.id))
    # the update page needs to be populated with current title and content
    elif request.method == 'GET':  
        form.title.data =post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post', 
                            form=form, legend ='Update Post')
    



# route for delete post 
@posts.route("/post/<int:post_id>/delete", methods =['POST'])
@login_required #login is required to update as we only need a user to delete a post
def delete_post(post_id):
    post =Post.query.get_or_404(post_id)
    #now we need to make it in a way that only the person who wrote the post can delete it 
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('main.home'))