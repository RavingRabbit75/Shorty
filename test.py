from app import app, db, User
from flask_testing import TestCase
import unittest

class BaseTestCase(TestCase):
    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///bitlyClone.db'
        return app

    def setUp(self):
        db.create_all()
        user1 = User("gregm")
        user2 = User("rayc")
        db.session.add_all([user1, user2])
        db.session.commit()

    def teardown(self):
        db.drop_all()

    def test_index(self):
        response = self.client.get('/users', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'gregm', response.data)
        self.assertIn(b'rayc', response.data)

    def test_show(self):
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(
            '/users',
            data=dict(username='New')
            )
        self.assertIn(b'gregm', response.data)

    def test_edit(self):
        response = self.client.get(
            '/users/1/edit'
        )
        self.assertIn(b'gregm', response.data)

    def test_update(self):
        response = self.client.get(
            '/users/1',
            data=dict(username="updated"),
            follow_redirects=True
        )
        self.assertIn(b"updated", response.data)
        self.assertNotIn(b"gregm", response.data)

    def test_delete(self):
        response = self.client.delete(
            '/users/1',
            follow_redirects=True
        )
        self.assertNotIn(b'gregm', response.data)



if __name__ == '__main__':
    unittest.main()