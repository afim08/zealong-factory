from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired





#form for new post 
class PostForm(FlaskForm):
    title =StringField('Title',validators= [DataRequired()])
    content =TextAreaField('Content',validators =[DataRequired()])
    submit =SubmitField('Post')
#an instance of this form will be created in the route
#and pass it into create_post.html template
