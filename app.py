from flaskblog import create_app

app= create_app()
#if we run ' set FLASK_DEBUG = 1 ' or export FLASK_DEBUG=1' in  mac
# in the cmd, then we wont need to stop and rerun the server to 
#display the changes made
if __name__ == '__main__':
    app.run(debug=True, port =39199)
