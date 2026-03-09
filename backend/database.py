import sqlite3
DB_PATH = "data/feedback.db"
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt_text TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt_id INTEGER,
    response_text TEXT,
    bert_score REAL,
    rouge_score REAL,
    is_selected INTEGER DEFAULT 0
)
""")
    conn.commit()
    conn.close()
def save_prompt(prompt_text):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO prompts (prompt_text) VALUES (?)",
        (prompt_text,)
    )

    prompt_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return prompt_id
def save_responses(prompt_id, responses, bert_scores, rouge_scores):
    conn = get_connection()
    cursor = conn.cursor()

    for i, response in enumerate(responses):
        cursor.execute(
            """
            INSERT INTO responses 
            (prompt_id, response_text, bert_score, rouge_score)
            VALUES (?, ?, ?, ?)
            """,
            (prompt_id, response, bert_scores[i], rouge_scores[i])
        )

    conn.commit()
    conn.close()
def get_responses_by_prompt(prompt_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, response_text, bert_score, rouge_score, is_selected
        FROM responses
        WHERE prompt_id = ?
        """,
        (prompt_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    responses = []

    for r in rows:
        responses.append({
            "response_id": r[0],
            "response_text": r[1],
            "bert_score": r[2],
            "rouge_score": r[3],
            "is_selected": r[4]
        })

    return responses
def select_best_response(response_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT prompt_id FROM responses WHERE id=?",
        (response_id,)
    )
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return False
    prompt_id = row[0]
    cursor.execute(
    "UPDATE responses SET is_selected=0 WHERE prompt_id=?",
    (prompt_id,)
)

    cursor.execute(
    "UPDATE responses SET is_selected=1 WHERE id=?",
    (response_id,)
)
    conn.commit()
    conn.close()

    return True
def get_all_prompts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM prompts")
    rows = cursor.fetchall()
    conn.close()
    prompt_ids = [r[0] for r in rows]

    return prompt_ids