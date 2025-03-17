from flask import Blueprint, render_template, request, send_from_directory
import os
import json
import random

# Create Blueprint for the Geography game
geography_bp = Blueprint("geography", __name__, url_prefix="/geography")

# Define the paths for game data and flags
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")
FLAGS_DIR = os.path.join(os.path.dirname(__file__), "UN_Flags")  # Ensure this matches your file structure

# Load game data
with open(DATA_PATH, "r", encoding="utf-8") as file:
    GAME_DATA = json.load(file)

def get_question():
    """Generate a random question with one correct and two incorrect flags."""
    correct_entry = random.choice(GAME_DATA)  # Pick a correct country
    wrong_entries = random.sample([c for c in GAME_DATA if c != correct_entry], 2)  # Pick two incorrect ones

    # Structure the answer choices
    options = [
        {"country": correct_entry["country"], "flag": correct_entry["file"], "correct": True},
        {"country": wrong_entries[0]["country"], "flag": wrong_entries[0]["file"], "correct": False},
        {"country": wrong_entries[1]["country"], "flag": wrong_entries[1]["file"], "correct": False},
    ]
    random.shuffle(options)  # Shuffle the answer order
    return correct_entry["country"], correct_entry["file"], options

@geography_bp.route("/", methods=["GET", "POST"])
def index():
    """Handles displaying questions and processing answers."""
    result = None  # Default to no result

    # If the user submitted an answer
    if request.method == "POST":
        selected_flag = request.form.get("selected_flag")  # Get the selected flag
        correct_flag = request.form.get("correct_flag")  # Get the correct answer

        result = selected_flag == correct_flag  # Check correctness

    # Generate a new question
    country, correct_flag, options = get_question()

    return render_template("geography.html", country=country, options=options, correct_flag=correct_flag, result=result)

@geography_bp.route("/flags/<path:filename>")  # Allow serving images from subfolders
def get_flag(filename):
    """Serve flag images from the UN_Flags folder."""
    return send_from_directory(FLAGS_DIR, filename)
