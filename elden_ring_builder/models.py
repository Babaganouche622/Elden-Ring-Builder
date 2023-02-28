# Create your models here.
from elden_ring_builder.extensions import db
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class Build(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  description = db.Column(db.String(500), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', back_populates='builds')
  weapon = db.relationship('Weapon', secondary='build_weapon', back_populates='build')


  def __repr__(self):
    return self.name


class Weapon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  image = db.Column(db.String(500), nullable=False)
  build = db.relationship('Build', secondary='build_weapon', back_populates='weapon')

  def __repr__(self):
    return self.name

build_weapon = db.Table('build_weapon',
  db.Column('build_id', db.ForeignKey('build.id')),
  db.Column('weapon_id', db.Integer, db.ForeignKey('weapon.id'))
)


# class Armor(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(50), nullable=False)
#   image = db.Column(db.String(500), nullable=False)
#   pass


class User(db.Model, UserMixin):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    builds = db.relationship('Build', back_populates='user')

    def __repr__(self):
      return self.username

