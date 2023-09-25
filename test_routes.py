import unittest
from app import app, db, Person

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask app and create a test client
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'  # Use a test database
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        # Clean up after the tests
        with app.app_context():
            db.drop_all()

    def setUp(self):
        # Create a test user before each test
        with app.app_context():
            db.create_all()
            user = Person(first_name="Test", last_name="User", img_url="test.jpg")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        # Clean up the test user after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_userDir(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_showForm(self):
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)

    def test_newPerson(self):
        response = self.client.post('/users/new', data=dict(first_name="John", last_name="Doe", img_url="john.jpg"))
        self.assertEqual(response.status_code, 302)  # Redirect after adding a new user

    def test_show_person(self):
        with app.app_context():
            user_id = Person.query.first().id
        response = self.client.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
