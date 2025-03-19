import os
import json
import random
import importlib.util
from flask import Blueprint, jsonify

game_bp = Blueprint("game", __name__)

GAMES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "games")

def load_game_config(game_name):
    """Loads game-specific settings from __init__.py."""
    game_folder = os.path.join(GAMES_FOLDER, game_name)
    game_init_path = os.path.join(game_folder, "__init__.py")

    if not os.path.exists(game_init_path):
        return None  # Game not found

    spec = importlib.util.spec_from_file_location("game_config", game_init_path)
    game_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(game_config)

    return {
        "question_format": getattr(game_config, "QUESTION_FORMAT", "What is this?"),
        "answer_format": getattr(game_config, "ANSWER_FORMAT", "This is {answer}."),
        "photos_path": os.path.join(game_folder, getattr(game_config, "Photos", "./photos")),
        "json_path": os.path.join(game_folder, getattr(game_config, "JSON", "./data.json"))
    }

def load_game_data(json_path):
    """Loads the JSON data file specified in the game config."""
    if not os.path.exists(json_path):
        return None

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

@game_bp.route("/game/<game_name>/question", methods=["GET"])
def get_random_question(game_name):
    """Generates a random question for the selected game."""
    game_config = load_game_config(game_name)
    if not game_config:
        return jsonify({"error": "Game not found"}), 404

    data = load_game_data(game_config["json_path"])
    if not data:
        return jsonify({"error": "Game data not found"}), 404

    # Select one correct choice
    correct_choice = random.choice(data)

    # Select two incorrect choices
    wrong_choices = random.sample(
        [item for item in data if item["iso"] != correct_choice["iso"]], 2
    )

    # Shuffle answers
    choices = [correct_choice] + wrong_choices
    random.shuffle(choices)

    # Format question and answer
    question_text = game_config["question_format"].format(country=correct_choice["country"])
    answer_text = game_config["answer_format"].format(country=correct_choice["country"], flag=correct_choice["iso"])

    return jsonify({
        "question": question_text,
        "correct_answer": correct_choice["iso"],
        "answer_text": answer_text,
        "choices": [
            {"iso": flag["iso"], "file": os.path.join(game_config["photos_path"], flag["iso"] + ".png")}
            for flag in choices
        ]
    })
