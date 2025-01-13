import sqlite3

DB_PATH = 'database/app_database.db'

def initialize_database():
    """
    Initializes the SQLite database by creating required tables if they don't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            input_data TEXT,
            prediction_result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Create additional tables if needed

    conn.commit()
    conn.close()

def add_prediction(user_id, input_data, prediction_result):
    """
    Adds a prediction record to the database.

    Args:
        user_id (int): The ID of the user making the prediction.
        input_data (str): The input data used for prediction.
        prediction_result (str): The result of the prediction.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO predictions (user_id, input_data, prediction_result)
        VALUES (?, ?, ?)
    ''', (user_id, input_data, prediction_result))

    conn.commit()
    conn.close()

def fetch_user_predictions(user_id):
    """
    Fetches all predictions made by a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dictionaries containing predictions.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, input_data, prediction_result, timestamp
        FROM predictions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()

    predictions = [
        {
            "id": row[0],
            "input_data": row[1],
            "prediction_result": row[2],
            "timestamp": row[3]
        }
        for row in rows
    ]

    return predictions

def fetch_user_id(username):
    """
    Fetches the user ID for a given username.

    Args:
        username (str): The username.

    Returns:
        int: The user ID, or None if the user does not exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None
