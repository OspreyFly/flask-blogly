from flask import Flask, render_template, request, redirect
from models import db, connect_db, Person

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

@app.route("/user_listing")
def userDir():
    users = Person.query.all()
    return render_template("users.html", users=users)

@app.route("/add_person")
def showForm():
    return render_template("user_new_form.html")

@app.route("/add_person", methods=["POST"])
def addPerson():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    person = Person(first_name, last_name, img_url)
    
    db.session.add(person)
    db.session.commit()

    return redirect(f"/{person.id}")
    

@app.route("/<int:person_id>")
def show_person(person_id):
    person = Person.query.get_or_404(person_id)
    return render_template("user_detail_page.html", person=person)


