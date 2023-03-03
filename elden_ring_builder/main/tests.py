import os
import unittest
import app

from datetime import date
from elden_ring_builder.extensions import app, db, bcrypt
from elden_ring_builder.models import Build, Weapon, User
"""
Run these tests with the command:
python3 -m unittest elden_ring_builder.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
  password_hash = bcrypt.generate_password_hash('Goochie').decode('utf-8')
  user = User(username='Dinkleberry', password=password_hash)
  db.session.add(user)
  db.session.commit()

def create_build():
  build = Build(
    name='Test Build',
    description='This is a test build',
    user_id = User.query.filter_by(username='Dinkleberry').first().id,
    user = User.query.filter_by(username='Dinkleberry').first()
  )
  db.session.add(build)
  db.session.commit()

def create_weapon():
  weapon = Weapon(
    name='Test Weapon',
    image='https://talbotspy.org/files/2016/02/Screen-Shot-2016-02-24-at-9.24.44-AM.jpg'
  )
  db.session.add(weapon)
  db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
  """Tests for main routes."""

  def setUp(self):
    """Executed prior to each test."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    self.app = app.test_client()
    db.drop_all()
    db.create_all()

  def test_homepage_logged_out(self):
    """Test that the homepage shows Builds and Weapons and Users when logged out."""
    create_user()
    create_weapon()
    create_build()

    response = self.app.get('/', follow_redirects=True)
    response_text = response.get_data(as_text=True)

    # Test should show these things
    self.assertIn('Test Build', response_text)
    self.assertIn('Test Weapon', response_text)
    self.assertIn('Dinkleberry', response_text)
    self.assertIn('Log In', response_text)
    self.assertIn('Sign Up', response_text)

    # Test should not show these things
    self.assertNotIn('Create Build', response_text)
    self.assertNotIn('Create Weapon', response_text)
    self.assertNotIn('Profile', response_text)

  def test_create_weapon(self):
    """Test that the create weapon page works when logged in."""
    create_user()
    login(self.app, 'Dinkleberry', 'Dinkleberry')

    # enter the create weapon page and enter form data to make a new weapon
    response = self.app.post('/create_weapon', data=dict(
      name='Test Weapon',
      image='https://talbotspy.org/files/2016/02/Screen-Shot-2016-02-24-at-9.24.44-AM.jpg'
    ), follow_redirects=True)
    response_text = response.get_data(as_text=True)

    self.assertIn('Test Weapon', response_text)
    self.assertIsNotNone(Weapon.query.filter_by(name='Test Weapon').first())

  def test_create_build(self):
    """Test that the user can create a new build after they are logged in."""
    create_user()
    login(self.app, 'Dinkleberry', 'Goochie')
    
    
    self.assertIn
    response = self.app.post('/create_build', data=dict(
      name='Test Build',
      description='This is a test build'
    ), follow_redirects=True)
    response_text = response.get_data(as_text=True)


