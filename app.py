from flask import Flask, render_template, request, redirect
from models import db, connect_db, Person, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretKEY"

connect_db(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route("/users")
def userDir():
    users = Person.query.all()
    return render_template("users.html", users=users)

@app.route("/users/new", methods=["GET"])
def showForm():
    return render_template("user_new_form.html")

@app.route("/users/new", methods=["POST"])
def newPerson():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']
    person = Person(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(person)
    db.session.commit()
    return redirect(f"/users/{person.id}")
    
@app.route("/users/<int:person_id>")
def show_person(person_id):
    user = Person.query.get_or_404(person_id)
    posts = Post.query.filter_by(author_id = person_id).all()
    return render_template("user_detail_page.html", user=user, posts=posts)

@app.route("/users/<int:person_id>/edit", methods=["GET"])
def edit_person_get(person_id):
    person = Person.query.get_or_404(person_id)
    return render_template("user_edit_page.html", person=person)

@app.route("/users/<int:person_id>/edit", methods=["POST"])
def edit_person_post(person_id):
    person = Person.query.get_or_404(person_id)
    person.first_name = request.form['first_name']
    person.last_name = request.form['last_name']
    person.img_url = request.form['img_url']
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:person_id>/delete", methods=["POST"])
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return redirect("/users")

"""HANDLE POSTS"""

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def showPostForm(user_id):
    user = Person.query.get_or_404(user_id)
    return render_template("post_new_form.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def newPost(user_id):
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, author_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post.id}")
    
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail_page.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post_get(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_edit_page.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")
