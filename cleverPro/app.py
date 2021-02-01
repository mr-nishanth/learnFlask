from datetime import datetime
from flask import Flask
from flask import render_template
from flask import url_for , request , redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# /// is crt dir and //// is root dir
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///posts.db'

# craete database
db = SQLAlchemy(app)
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False , default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)
# database end

    def __repr__(self):
        return f"Blog post {self.id}"

@app.route("/")
def home():
    return render_template("index.html")

# Insert
@app.route("/posts/new",methods=["GET","POST"])
def new_post():
    if request.method == "POST":
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


# Read
@app.route("/posts",methods=["GET","POST"])
def posts():
    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("posts.html",posts=all_posts)

# edit or update
@app.route('/posts/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)

# Delete
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')



if __name__ == "__main__":
    app.run(debug=True)
