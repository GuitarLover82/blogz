from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode!@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True # useful for debugging issues you may have when your application isn't talking to your database the way you expect it to
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))

    def __init__(self, title, body ):
        self.title = title
        self.body = body


@app.route("/blog", methods=['GET', 'POST'])
def blog():
    return render_template('/blog.html')


@app.route("/newpost", methods=['GET', 'POST'])
def newpost():
    return render_template('/newpost.html')    



if __name__ == '__main__':
    app.run()