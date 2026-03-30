from flask_sqlalchemy import SQLAlchemy

# This file defines the data models for the Trivia Game application.
# Every model here becomes a table in the database.
# db is the single shared database instance — all models and auth.py import from here.

db = SQLAlchemy()


# ─────────────────────────────────────────────────────────────
# User model — maps to the existing 'Users' table in flag_game.db
# __tablename__ tells SQLAlchemy the real table name (Users, not user)
# ─────────────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    # Column is called password_hash in the DB — plain text for now (educational project)
    password_hash = db.Column(db.String(255), nullable=False)

    # Optional fields — all have defaults in the DB so we don't need to set them
    photo_url = db.Column(db.String(255))
    elo_rating = db.Column(db.Integer, default=1200)
    games_played = db.Column(db.Integer, default=0)
    registration_date = db.Column(db.Date)
    social_links = db.Column(db.Text)
    sex = db.Column(db.String(10))
    created_games = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

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