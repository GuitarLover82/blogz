from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:launchcode!@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)
app.secret_key = 'ihavenosecrets'

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner ):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
        elif user and user.password != password:
            flash("Password is incorrect", "error") 
            return render_template('login.html')  
        else:
            flash("Username does not exist", "error")
            return render_template('login.html')

    else:
        return render_template("login.html")



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    if request.method == 'POST':

        username_error = ""
        password_error = ""
        verify_password_error = "" 

        username = request.form['username']
        password = request.form['password']
        verfy_password = request.form['verify_password']
        existing_username = User.query.filter_by(username=username).first()

        if verfy_password == "":
            verify_password_error = "That's not a valid password"
        elif verfy_password != password:
            verify_password_error = "Passwords don't match"

        if password == "":
            password_error = "That is not a valid password"
        elif len(password) < 3:
            password_error = "That is not a valid password"

        if username == "":
            username_error = "That is not a valid username"
        elif len(username) < 3:
            username_error = "That is not a valid username"
        elif existing_username:
            username_error = "That username already exists"    

        if not username_error and not password_error and not verify_password_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
            
        else:
            return render_template('signup.html', username=username, username_error=username_error, password_error=password_error, verify_password_error=verify_password_error)

    else:
        return render_template('signup.html')




@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')  

@app.route("/blog", methods=['GET', 'POST'])
def blog():

    blog_id = request.args.get('id')
    blog_user = request.args.get('user')
    if blog_id != None:
        blog_entry = Blog.query.filter_by(id=blog_id).first()
        return render_template('blog_entry.html', blog_entry=blog_entry)

    if blog_user != None:
        user = User.query.filter_by(username=blog_user).first()
        blog_entry = Blog.query.filter_by(owner=user).all()
        return render_template('singleUser.html', blog_entry=blog_entry, username=blog_user)

    else:
        blog_entry = Blog.query.all()
        return render_template('blog.html', blog_entry=blog_entry)

    


@app.route("/newpost", methods=['GET', 'POST'])
def newpost():

    if request.method == 'POST':
        blog_title_error = ""
        blog_body_error = ""
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        
        if body == "":
            blog_body_error = 'Please fill in the body'
        if title == "":
            blog_title_error = 'Please fill in the title'
        if not blog_body_error and not blog_title_error:
            new_entry = Blog(title, body, owner)
            db.session.add(new_entry)
            db.session.commit()
            id = new_entry.id
            return redirect('/blog?id={}'.format(id))
        else:
            return render_template('newpost.html', title=title, body=body, 
            blog_title_error=blog_title_error, blog_body_error=blog_body_error)

    else:
        return render_template('newpost.html')





if __name__ == '__main__':
    app.run()