from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcode!@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True 
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(1500))

    def __init__(self, title, body ):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')

@app.route("/blog", methods=['GET', 'POST'])
def blog():

    blogs = Blog.query.all()
    blog_id = request.args.get('id')
    if blog_id != None:
        blog = Blog.query.get(blog_id)
        return render_template('blog_entry.html', blog=blog)
    
    return render_template('blog.html', blogs=blogs)

    


@app.route("/newpost", methods=['GET', 'POST'])
def newpost():

    blog_title_error = ""
    blog_body_error = ""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        if body == "":
            blog_body_error = 'Please fill in the body'
        if title == "":
            blog_title_error = 'Please fill in the title'
        if not blog_body_error and not blog_title_error:
            new_entry = Blog(title, body)
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