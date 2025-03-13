from flask_sqlalchemy import SQLAlchemy

# This file defines the data models for the Trivia Game application.
# These models represent the structure of the database tables and the relationships between them.

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    answer_text = db.Column(db.String(500), nullable=False)

    category = db.relationship('Category', backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return f'<Question {self.question_text}>'