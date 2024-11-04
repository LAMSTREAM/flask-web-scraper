from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Text, TIMESTAMP, ARRAY

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    sub = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    websites = db.relationship('Website', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.sub}, Email: {self.email}>'


class Website(db.Model):
    __tablename__ = 'website'

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ctime = db.Column(TIMESTAMP, server_default=db.func.now())
    mtime = db.Column(TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    website_url = db.Column(db.String, nullable=False)
    website_content = db.Column(Text, nullable=True)  # Stores HTML or text content as a string
    website_preview = db.Column(db.LargeBinary, nullable=True)    # Store the screenshot of the website
    questions = db.Column(ARRAY(Text), nullable=True)  # Array of text questions
    user_sub = db.Column(db.String, db.ForeignKey('user.sub'), nullable=False)

    analyses = db.relationship('Analysis', backref='website', lazy=True)

    def __repr__(self):
        return f'<Website {self.index}, URL: {self.website_url}>'


class Analysis(db.Model):
    __tablename__ = 'analysis'

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ctime = db.Column(TIMESTAMP, server_default=db.func.now())
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=True)
    website_index = db.Column(db.Integer, db.ForeignKey('website.index'), nullable=False)

    def __repr__(self):
        return f'<Analysis {self.index}, Question: {self.question}>'

