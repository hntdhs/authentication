import email
from enum import unique
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pdb


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)
    # pdb.set_trace()
    db.create_all()

class User(db.Model):

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    # why is username following a different format?

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
    # no idea what the cascade thing is
    # cascading delete - users and user feedback. if yuo delete user and not their feedback you end up with a foreign key leading to non existent row

    # solution code says next is the start of convenience class methods - what is that?

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        # I'm assuming this is accessing those arguments from right above, but what is cls?
        # probably giving the class name
        """registers a user and hashes their password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """makes sure user is in system and password is correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

        # I don't understand how these class methods are used by other files - looking at the login route in app.py, where is the authentication method being incorporated?

class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )