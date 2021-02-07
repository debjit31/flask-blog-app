from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ctnmetixewemsl:5fb2f05591ca20697c86c8e7ade81b51446a2334493ba0ec81293a84ca448338@ec2-54-211-77-238.compute-1.amazonaws.com:5432/d8c6a9rp970cjj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.String(20))
    content = db.Column(db.Text)
    def __init__(self, title, subtitle, author, date_posted, content):
        self.title=title
        self.subtitle=subtitle
        self.author=author
        self.date_posted=date_posted.strftime('%B %d %Y')
        self.content=content

## home page
@app.route("/")
def index():
    posts = Blogpost.query.order_by(Blogpost.id.desc()).all()
    return render_template("index.html", posts=posts)

## create your own post
@app.route("/addPost")
def addPost():
    return render_template("add_post.html")


@app.route('/postdata', methods = ["POST"])
def postdata():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title,subtitle,author,datetime.now(),content)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id = post_id).one()
    return render_template("post.html", post = post)


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
