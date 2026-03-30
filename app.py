import sys
import os
from flask import Flask, render_template, request, session, redirect, url_for

# Ensure Flask can find 'games'
sys.path.append(os.path.join(os.path.dirname(__file__), "app", "games"))
# Ensure Flask can find 'app' folder (for models and auth)
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

# Import the Geography game Blueprint
from geography import geography_bp

# Import the Auth Blueprint (register, login, logout)
from auth import auth_bp

# Import db and all models so db.create_all() knows what tables to create
from models import db

app = Flask(__name__)

app.secret_key = "replace_this_with_a_random_secret_key"

# Tell SQLAlchemy where the database file is.
# sqlite:/// means a local file. trivia.db will be created in the app folder.
# Point to the single shared database — absolute path to avoid ambiguity
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "app", "games", "geography", "flag_game.db"
)

# Connect the db instance to this app
db.init_app(app)

# Register Blueprints
app.register_blueprint(geography_bp)
app.register_blueprint(auth_bp)

# Create all database tables if they don't exist yet.
# This runs once at startup — safe to leave in, it won't overwrite existing data.
with app.app_context():
    db.create_all()

# Home page
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name", "").strip()

        if action == "submit_name":
            if name.lower() == "db":
                # Reserved name — ask if they want to login
                return render_template("home.html", mode="login_prompt")
            elif name:
                # Valid name — ask: guest or register?
                session["temp_name"] = name
                return render_template("home.html", mode="guest_or_register", name=name)
            else:
                return render_template("home.html", mode="name_entry", error="Please enter a name.")

        elif action == "play_guest":
            # Save the name and go to the game selection
            session["player_name"] = session.pop("temp_name", "Guest")
            return redirect(url_for("home"))

        elif action == "choose_another":
            # User typed "db" but doesn't want to login — back to name entry
            return render_template("home.html", mode="name_entry")

    # If player already identified, show the game selection
    if "player_name" in session or "username" in session:
        return render_template("home.html", mode="hub")

    # First visit — show name entry
    return render_template("home.html", mode="name_entry")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
