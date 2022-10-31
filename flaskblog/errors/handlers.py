#we are going to create a new blue print for errors
#hence we import Blueprint
from flask import Blueprint, render_template
#create a new instance of errors
#nae of the blueprint is given to be 'errors'
errors = Blueprint('errors',__name__)

#creating error handlers is similar to how we create routes
#except that we use different decorators

#error handler for 404 errors
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500