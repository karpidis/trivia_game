import sys
import os
from flask import Flask, render_template

# Ensure Flask can find 'games'
sys.path.append(os.path.join(os.path.dirname(__file__), "app", "games"))

# Import the Geography game Blueprint
from geography import geography_bp

app = Flask(__name__)

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret_key"
# Register the Geography Blueprint
app.register_blueprint(geography_bp)

# Home page with link to the Geography game
@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
