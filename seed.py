from models import Person, Post, Tag,  db
from app import app

# Create an application context
with app.app_context():
    # Drop and recreate the database tables
    db.drop_all()
    db.create_all()

    person1 = Person(first_name="Noah", last_name="Jones", img_url="https://wp.technologyreview.com/wp-content/uploads/2022/12/E8G1GY.jpeg")
    person2 = Person(first_name="Oliver", last_name="Jones", img_url="https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png")

    post1 = Post(title="Learning Web Development", content="I've been learning Web Development from Springboard. It has prepared me to use some of the most in-demand programming workflows.", author_id=1)
    post2 = Post(title="Meow", content="Scratch, scratch, scratch, MEOOOOOOOOOOOW!!!!!!!!", author_id=2)
    post3 = Post(title="Rawwr", content="I'm so fierce! Get me more food human.", author_id=2)

    tag1 = Tag(name="Comedy")
    tag2 = Tag(name="Scary")
    tag3 = Tag(name="Animals")
    tag4 = Tag(name="Social")

    db.session.add(person1)
    db.session.add(person2)

    db.session.commit()

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)

    db.session.commit()

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.add(tag4)

    db.session.commit()
