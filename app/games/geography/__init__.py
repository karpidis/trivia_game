from flask import Blueprint, render_template, request, send_from_directory, session
import os
import json
import random
from . import db

# Create Blueprint for the Geography game
geography_bp = Blueprint("geography", __name__, url_prefix="/geography")

# Define paths for game data and flags
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")
FLAGS_DIR = os.path.join(os.path.dirname(__file__), "UN_Flags")

# Load country-flag data from JSON file once at startup
with open(DATA_PATH, "r", encoding="utf-8") as file:
    GAME_DATA = json.load(file)

def get_question():
    """
    Select a correct country and two wrong ones, register question in DB,
    return everything needed to generate the question.
    """
    correct_entry = random.choice(GAME_DATA)
    wrong_entries = random.sample([c for c in GAME_DATA if c != correct_entry], 2)

    # Extract flags for DB and rendering
    correct_flag = correct_entry["file"]
    wrong1 = wrong_entries[0]["file"]
    wrong2 = wrong_entries[1]["file"]
    print(f"Correct: {correct_flag}, Wrong1: {wrong1}, Wrong2: {wrong2}")

    # Insert or update this question appearance in the DB
    db.insert_or_update_question(correct_flag, wrong1, wrong2)

    # Prepare the options to show to the user
    options = [
        {"country": correct_entry["country"], "flag": correct_flag, "correct": True},
        {"country": wrong_entries[0]["country"], "flag": wrong1, "correct": False},
        {"country": wrong_entries[1]["country"], "flag": wrong2, "correct": False},
    ]

    random.shuffle(options)
    return correct_entry["country"], correct_flag, wrong1, wrong2, options

def _render_new_question():
    """
    Generate a new question and save its data to session for secure checking later.
    """
    country, correct_flag, wrong1, wrong2, options = get_question()

    # Save necessary values to session (not visible to the browser)
    session["current_question"] = {
        "correct_flag": correct_flag,
        "wrong1": wrong1,
        "wrong2": wrong2,
        "country": country,
    }

    return render_template(
        "geography.html",
        mode="question",
        country=country,
        options=options,
        result=None
    )

@geography_bp.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the game logic:
    - GET: Show a new question
    - POST: Evaluate answer, log result, show next or correct answer
    """
    if request.method == "POST":
        selected_flag = request.form.get("selected_flag")
        correct_country = request.form.get("correct_country")

        # Load correct answer and wrong options from session
        q = session.get("current_question", {})
        correct_flag = q.get("correct_flag")
        wrong1 = q.get("wrong1")
        wrong2 = q.get("wrong2")

        # If any session value is missing, regenerate
        if not all([correct_flag, wrong1, wrong2]):
            return _render_new_question()

        is_correct = selected_flag == correct_flag

        # Log user's answer in the database
        db.update_question_results(correct_flag, wrong1, wrong2, selected_flag)

        if is_correct:
            # If correct, show next question with success message
            return _render_new_question()
        else:
            # If incorrect, show correct flag as feedback
            return render_template(
                "geography.html",
                mode="show_answer",
                correct_flag=correct_flag,
                correct_country=correct_country
            )

    # On GET: show a new question
    return _render_new_question()

@geography_bp.route("/flags/<path:filename>")
def get_flag(filename):
    """Serve flag image files."""
    return send_from_directory(FLAGS_DIR, filename)
