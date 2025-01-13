import sqlite3
from bcrypt import hashpw, gensalt, checkpw

# Database Connection
DB_PATH = 'database/app_database.db'

def signup_user(username, password):
    """
    Registers a new user with a hashed password.

    Args:
        username (str): The username for the new account.
        password (str): The plain text password for the new account.

    Returns:
        bool: True if signup was successful, False otherwise.
    """
    hashed_pw = hashpw(password.encode(), gensalt())
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    """
    Authenticates a user by checking their credentials.

    Args:
        username (str): The username.
        password (str): The plain text password.

    Returns:
        bool: True if credentials are valid, False otherwise.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()

    if record and checkpw(password.encode(), record[0]):
        return True
    return False

def is_authenticated():
    """
    Checks the session state to determine if the user is logged in.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    return "authenticated" in st.session_state and st.session_state["authenticated"]

def logout_user():
    """
    Logs out the current user by resetting session state.
    """
    st.session_state["authenticated"] = False
    st.session_state["username"] = ""
