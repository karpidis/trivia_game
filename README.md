📸 Photo Quiz Game Framework

A web-based quiz platform where players match names with images or images with names.
Built with extensibility in mind, the framework supports multiple game types, formats, and future expansion.

🚀 Overview

Photo Quiz Game Framework is designed as a modular system for building visual recognition quizzes.

It supports:

multiple game types (flags, faces, etc.)
multiple quiz formats
public and private datasets
future rating and difficulty systems

The first implemented version is the Flag Guessing Game, which serves as the foundation for the platform.

🎮 Game Formats

Each game can support one or more of the following formats:

1. Three Photos – One Name

A name is shown, and the player selects the correct image from three options.

2. Three Names – One Photo

An image is shown, and the player selects the correct name from three options.

3. One Photo – Write the Name

An image is shown, and the player types the correct name.
Aliases and alternative answers may be accepted.

🌍 Game Types
Flag Game (Implemented)
Match country names to flags
Default public game
Uses preloaded dataset
Face Game (Planned)
Match names to photos of people
Supports user-uploaded images and aliases
Data remains private unless explicitly shared
🔁 Game Flow
One question per round
After answering:
✅ Correct → next question immediately
❌ Incorrect → show correct answer → continue
Game ends when all questions are completed
⭐ Rating System (Planned)

Inspired by Elo rating logic.

Player Rating

Represents the player’s performance level.

Question Difficulty

Each question has a difficulty rating, treated like an opponent’s strength.

Rating Updates
Correct answers → rating increases
Incorrect answers → rating decreases
Magnitude depends on difficulty
Symmetric Elo-style updates
🌐 Public vs Private Games
Public Games
Use aggregated player data
Difficulty evolves based on global performance
Suspicious users have reduced influence
Private Games
Ratings and difficulty are local
No data sharing unless explicitly enabled
⚖️ Difficulty Logic

Each game defines its own difficulty model.

Flag Game

Difficulty depends on answer combinations, not just the correct answer.

Example:

Some incorrect options are more misleading than others
Face Game

Difficulty is tied to the specific person or image.

🚫 Invalid Combinations

To ensure fairness, certain combinations are excluded.

Flag Game

The following must never appear together:

Chad vs Romania
Monaco vs Indonesia
Face Game

Default rule:

Do not mix genders in the same question

Optional filters (configurable):

age similarity
ethnicity
background
group similarity (e.g. classmates)
✏️ In-Game Editing (Planned)

Users can:

flag mistakes during gameplay
rename photos
add/remove aliases
Behaviour
Private games → changes apply immediately
Public games → may require admin approval
📥 Data Import (Planned)

Users can create their own quiz datasets.

Import Process
Upload photos
Assign names
Optionally add aliases and metadata
Rules
Photos without names are rejected
Data is validated before use
Images are resized/cropped if needed
🧹 Data Validation

Before gameplay:

Ensure each photo has a valid name
Ignore corrupt or invalid files
Normalize image size and aspect ratio
Register aliases as valid answers
🌐 Deployment & Privacy
Hosted Platform
Runs in a browser
No installation required
Public Data
May contribute to global difficulty metrics
Private Data
Never shared without explicit consent
Local Network Support
Can run on local servers (schools, teams, offices)
✅ Current Implementation (MVP)
Flag Guessing Game
Format: Three Flags – One Country
Preloaded dataset (flags + countries)
One question per round
Immediate feedback and progression
Accessible via web browser
🔮 Planned Features
Gameplay
Additional formats (text input, reversed matching)
Face-based quizzes
Multiplayer modes
Leaderboards
Rating System
Player ranking (Elo-based)
Question difficulty tracking
Data & Flexibility
Alias support
Custom datasets
Import/export functionality
Fairness Controls
Invalid combination filtering
Optional similarity-based difficulty modes
Editing & Moderation
In-game corrections
Admin approval system
Accounts
User authentication (Google, Facebook, etc.)
Persistent progress and stats
🧠 Design Philosophy

Different quiz games should share the same core system,
while each game defines its own:

data
validation rules
difficulty logic
fairness constraints

This allows new game types to be added without redesigning the entire application.

⚙️ Tech Stack (Current)
Python
Flask
HTML / Templates
📌 Status

🚧 Work in progress
The core architecture is being stabilised while expanding gameplay features.
