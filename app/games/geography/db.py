import sqlite3    # Built-in SQLite driver
import os         # For filesystem path operations

# Path to your SQLite database file
DB_PATH = os.path.join(os.path.dirname(__file__), 'flag_game.db')

def question_exists(correct_flag, wrong1, wrong2):
    """
    Return one of:
    - "legal"   → exists and is legal (legal = 1)
    - "illegal" → exists and is marked illegal (legal = 0)
    - "new"     → does not exist in the DB yet
    """
    wrong1, wrong2 = sorted([wrong1, wrong2])
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT legal
          FROM Questions
         WHERE correct_flag = ?
           AND option_flag1 = ?
           AND option_flag2 = ?
         LIMIT 1
    """, (correct_flag, wrong1, wrong2))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return False
    return "legal" if row[0] == 1 else "illegal"


def insert_or_update_question(correct_flag, wrong1, wrong2): #dict for arguments, 
    #better name upsert_question
    """
    Ensure the question is in the database and update its times_appeared.
    If it doesn't exist, insert it with times_appeared=1.
    If it does, increment times_appeared by 1 and reset legal=1.
    """
    # 1) Determine whether this question already exists
    exists = question_exists(correct_flag, wrong1, wrong2)
    
    if exists == "illegal":
        return None
    # 2) Delegate to the updater
    update_questions_db(exists, correct_flag, wrong1, wrong2)

def update_questions_db(exists, correct_flag, wrong1, wrong2):
    """
    Insert or update the Questions table:
      - On first-ever appearance: INSERT with times_appeared = 1
      - On subsequent appearances: UPDATE times_appeared += 1
    """
    # Keep the wrong flags sorted
    wrong1, wrong2 = sorted([wrong1, wrong2])

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    if not exists:
        # 1st time we see this exact question: set times_appeared to 1
        cur.execute("""
            INSERT INTO Questions (
                correct_flag,
                option_flag1,
                option_flag2,
                times_appeared
            ) VALUES (?, ?, ?, 1)
        """, (correct_flag, wrong1, wrong2))
    else:
        # Already exists → bump times_appeared by 1 and ensure legal=1
        cur.execute("""
            UPDATE Questions
               SET times_appeared = times_appeared + 1,
                   legal           = 1
             WHERE correct_flag = ?
               AND option_flag1 = ?
               AND option_flag2 = ?
        """, (correct_flag, wrong1, wrong2))
        
    conn.commit()
    conn.close()
    return True


def delete_question(correct_flag, wrong1, wrong2):
    """
    Remove the question row matching (correct_flag, wrong1, wrong2).
    """
    # Keep wrong flags in alphabetical order to match storage
    wrong1, wrong2 = sorted([wrong1, wrong2])

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    cur.execute("""
        DELETE FROM Questions
         WHERE correct_flag = ?
           AND option_flag1 = ?
           AND option_flag2 = ?
    """, (correct_flag, wrong1, wrong2))

    conn.commit()
    conn.close()


def update_question_results(correct_flag, wrong1, wrong2, selected_flag):
    """
    Increment the “chosen” counter on the Questions row that matches
    (correct_flag, wrong1, wrong2).  Assumes that row already exists.

    - If selected_flag == correct_flag:   correct_flag_chosen += 1
    - If selected_flag == wrong1:         option_flag1_chosen += 1
    - If selected_flag == wrong2:         option_flag2_chosen += 1
    """
    # Keep the wrong flags sorted
    wrong1, wrong2 = sorted([wrong1, wrong2])

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # Determine which column to bump
    if selected_flag == correct_flag:
        column = "correct_flag_chosen"
    elif selected_flag == wrong1:
        column = "option_flag1_chosen"
    elif selected_flag == wrong2:
        column = "option_flag2_chosen"
    else:
        conn.close()
        raise ValueError(f"selected_flag {selected_flag} not in question options")

    # Run a single UPDATE that increments the right column
    cur.execute(f"""
        UPDATE Questions
           SET {column} = {column} + 1 
         WHERE correct_flag = ?
           AND option_flag1 = ?
           AND option_flag2 = ?
    """, (correct_flag, wrong1, wrong2))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    correct_flag   = "GER"
    wrong1, wrong2 = "GRE", "USA"
    selected_flag  = "GER"

    # 0) Clean up any old test question first
    delete_question(correct_flag, wrong1, wrong2)

    # 1) Before anything, does the question exist?
    print("Exists before:", question_exists(correct_flag, wrong1, wrong2))

    # 2) Register that the question appeared
    insert_or_update_question(correct_flag, wrong1, wrong2)

    # 3) Now it surely exists
    print("Exists after insertion:", question_exists(correct_flag, wrong1, wrong2))

    # 4) Show its full row
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("""
        SELECT question_id, correct_flag, option_flag1, option_flag2,
               times_appeared, correct_flag_chosen, option_flag1_chosen, option_flag2_chosen
          FROM Questions
         WHERE correct_flag=? AND option_flag1=? AND option_flag2=?
    """, (correct_flag, wrong1, wrong2))
    row = cur.fetchone()
    print("Row after first appearance:", row)
    conn.close()

    # 5) Simulate the user clicking “GER” (correct)
    update_question_results(correct_flag, wrong1, wrong2, selected_flag)

    # 6) Show the row again to see the increments
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("""
        SELECT times_appeared, correct_flag_chosen, option_flag1_chosen, option_flag2_chosen
          FROM Questions
         WHERE correct_flag=? AND option_flag1=? AND option_flag2=?
    """, (correct_flag, wrong1, wrong2))
    updated = cur.fetchone()
    print("Row after answering:", updated)
    conn.close()

    # 7) And finally delete it so next run starts fresh
    delete_question(correct_flag, wrong1, wrong2)