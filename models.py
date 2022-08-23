"""Models for Stock app."""

from flask_bcrypt import Bcrypt
from re import I
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()



class User(db.Model):
    """Create User's table."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key = True, 
        autoincrement = True
    )

    username = db.Column(
        db.String(30), 
        nullable = False, 
        unique = True
    )
    
    password = db.Column(
        db.Text,
        nullable=False,
    )

    @classmethod
    def register(cls, username, pwd):
        """Register a user"""

        hashed = bcrypt.generate_password_hash(pwd)

        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate user's password and name are correct"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Profile(db.Model):
    """User Creates profile for their stocks."""

    __tablename__ = "profile"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    #stock ticker, such as TSLA
    favo = db.Column(
        db.String(30), 
        nullable = False 
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    user = db.relationship('User', backref="profile")

    def __init__(self, favo, user_id):
        self.favo = favo
        self.user_id = user_id
 


class Stock_table:
    """Show user the stock they saved."""

    __tablename__ = "stock"

    stock_id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    favorite = db.Column(
        db.Integer,
        db.ForeignKey('profile.id', ondelete="cascade")
    )

    tiker = db.Column(
        db.String(30), 
        nullable = False, 
        unique = True       
    )

    #How many stocks owned
    stock_num = db.Column(
        db.Integer
    )

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)