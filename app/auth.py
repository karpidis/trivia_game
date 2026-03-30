# ─────────────────────────────────────────────────────────────
# auth.py — Handles user registration and login
#
# We import db and User from models.py because that is where
# the single shared database instance lives. If we created a
# new SQLAlchemy() here it would be a completely separate
# connection and nothing would work.
# ─────────────────────────────────────────────────────────────

from flask import Blueprint, request, redirect, url_for, render_template, session
from models import db, User

# A Blueprint is a mini-application. It lets us keep auth routes
# in this file instead of cluttering app.py.
# We register it in app.py with: app.register_blueprint(auth_bp)
auth_bp = Blueprint('auth', __name__)


# ─────────────────────────────────────────────────────────────
# REGISTER
# GET  /register  → show the registration form
# POST /register  → process the form the user submitted
# ─────────────────────────────────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    # When the user just visits /register in the browser it is a GET.
    # We only show them the empty form.
    if request.method == 'GET':
        return render_template('register.html')

    # When the user fills the form and clicks Submit it becomes a POST.
    # request.form holds everything the user typed in the form fields.
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    # Basic check: make sure neither field is empty.
    if not username or not password:
        return render_template('register.html', error='Please fill in all fields.')

    # Ask the database: is there already a user with this username?
    # .first() returns the user if found, or None if not found.
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        # Username taken — show the form again with an error message.
        return render_template('register.html', error='Username already exists.')

    # Username is free — create a new User object.
    # Password is stored as plain text for now (educational project).
    new_user = User(username=username, password_hash=password)

    # db.session is like a shopping basket.
    # add() puts the new user in the basket.
    # commit() saves everything in the basket to the actual database.
    db.session.add(new_user)
    db.session.commit()

    # Registration successful — send the user to the login page.
    # We use redirect() instead of render_template() here because
    # if the user refreshes the page after a POST it would submit
    # the form again. A redirect avoids that problem.
    return redirect(url_for('auth.login'))


# ─────────────────────────────────────────────────────────────
# LOGIN
# GET  /login  → show the login form
# POST /login  → check the credentials the user submitted
# ─────────────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return render_template('login.html', error='Please fill in all fields.')

    # Look up the user in the database by username.
    user = User.query.filter_by(username=username).first()

    # Check two things:
    # 1. Did we find a user with that username?
    # 2. Does the password match?
    if not user or user.password_hash != password:
        # We give a vague message on purpose — we do not want to tell
        # an attacker whether the username or the password was wrong.
        return render_template('login.html', error='Invalid username or password.')

    # Credentials are correct.
    # Save the user's id in the session so we remember who is logged in
    # across all future requests.
    # session is like a small locker tied to the browser. Flask signs
    # it with SECRET_KEY so the user cannot tamper with it.
    session['user_id'] = user.user_id
    session['username'] = user.username

    return redirect(url_for('home'))


# ─────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():

    # Remove the user from the session.
    # pop() removes the key if it exists and does nothing if it does not,
    # so we will never get an error even if the user was not logged in.
    session.pop('user_id', None)
    session.pop('username', None)

    return redirect(url_for('home'))
