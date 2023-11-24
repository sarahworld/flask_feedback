from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users";

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    username = db.Column(db.String(20),
                         unique=True,
                         primary_key=True, nullable=False)
    
    password = db.Column(db.String,
                        nullable=False)
    
    email = db.Column(db.String(50),
                    nullable=False,
                    unique=True)
    
    first_name = db.Column(db.String(30),
                    nullable=False)
    
     
    last_name = db.Column(db.String(30),
                    nullable=False)
    
    @classmethod
    def register(cls, username, pwd):

        hashed_password = bcrypt.generate_password_hash(pwd);
        hashed_utf8 = hashed_password.decode("utf-8")

        return cls(username=username, password=hashed_utf8)
    

    @classmethod
    def authenticate(cls, username, pwd):

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False
        
class Feedback(db.Model):
    __tablename__="feedbacks"

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.String, nullable=False)
    
    username = db.Column(db.String,
                    db.ForeignKey('users.username'), nullable=False)