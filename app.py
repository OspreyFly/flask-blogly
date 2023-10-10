from flask import Flask, render_template, request, redirect
from models import db, connect_db, Person, Post, Tag, PostTag

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
    tags = Tag.query.all()
    return render_template("post_new_form.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def newPost(user_id):
    tags = request.form.getlist("tags[]")

    title = request.form['title']
    content = request.form['content']
    author_id = user_id 

    post = Post(title=title, content=content, author_id=author_id)
    db.session.add(post)
    db.session.commit()

    selected_tags = []
    for tag in tags:
        tag = Tag.query.filter_by(name=tag).first()
        if tag is not None:
            selected_tags.append(tag)

    post.tags.extend(selected_tags)
    db.session.commit()

    return redirect(f"/posts/{post.id}")
    
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    author = Person.query.get_or_404(post.author_id)
    tags = post.tags
    return render_template("post_detail_page.html", post=post, author=author, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post_get(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    all_tags = Tag.query.all()
    
    return render_template("post_edit_page.html", post=post, tags=tags, all_tags=all_tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        return "Post not found", 404

    post.title = request.form['title']
    post.content = request.form['content']

    tag_names = request.form.getlist("tags[]")

    post.tags.clear()

    selected_tags = []
    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        selected_tags.append(tag)

    for tag in selected_tags:
        if tag not in post.tags:
            post.tags.append(tag)

    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")


"""Handle Tags"""

@app.route("/tags")
def tagDir():
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_detail_page.html", tag=tag, posts=posts)

@app.route("/tags/new")
def showTagForm():
    return render_template("tag_new_form.html")

@app.route("/tags/new", methods=["POST"])
def newTag():
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tag.id}")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_get(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_edit_page.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag_post(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.commit()
    return redirect(f"/tags/{tag_id}")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")