import sys
import os

# Ensure Flask can find 'games'
sys.path.append(os.path.join(os.path.dirname(__file__), "games"))

from geography import geography_bp  # Import Blueprint

from flask import Flask

app = Flask(__name__)

# Register the Geography game Blueprint
app.register_blueprint(geography_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
