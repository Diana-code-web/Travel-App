import sqlite3
import bcrypt
import os

DB_PATH = "travel_assistant.db"


def init_db():
    """Create all database tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            UserID      INTEGER PRIMARY KEY AUTOINCREMENT,
            Name        VARCHAR(100) NOT NULL,
            Email       VARCHAR(150) NOT NULL UNIQUE,
            Password    VARCHAR(255) NOT NULL,
            CreatedAt   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Preferences table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            PreferenceID  INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID        INTEGER NOT NULL,
            DestType      VARCHAR(50),
            BudgetRange   VARCHAR(50),
            Interests     TEXT,
            FOREIGN KEY (UserID) REFERENCES users(UserID)
        )
    """)

    # Itineraries table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS itineraries (
            ItineraryID    INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID         INTEGER NOT NULL,
            Destination    VARCHAR(150),
            StartDate      DATE,
            EndDate        DATE,
            GeneratedPlan  TEXT,
            CreatedAt      DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (UserID) REFERENCES users(UserID)
        )
    """)

    conn.commit()
    conn.close()


def register_user(name, email, password):
    """
    Register a new user.
    Returns (True, 'success') or (False, 'error message').
    """
    if not name or not email or not password:
        return False, "All fields are required."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."

    # Hash password with bcrypt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute(
            "INSERT INTO users (Name, Email, Password) VALUES (?, ?, ?)",
            (name.strip(), email.strip().lower(), hashed.decode("utf-8"))
        )
        conn.commit()
        user_id = cur.lastrowid
        conn.close()
        return True, user_id

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists. Please log in."
    except Exception as e:
        return False, f"Registration failed: {str(e)}"


def login_user(email, password):
    """
    Authenticate a user.
    Returns (True, user_dict) or (False, 'error message').
    """
    if not email or not password:
        return False, "Please enter your email and password."

    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute(
            "SELECT UserID, Name, Email, Password FROM users WHERE Email = ?",
            (email.strip().lower(),)
        )
        row = cur.fetchone()
        conn.close()

        if row is None:
            return False, "No account found with this email. Please register."

        user_id, name, user_email, stored_hash = row

        # Verify password
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return True, {
                "user_id":  user_id,
                "name":     name,
                "email":    user_email,
            }
        else:
            return False, "Incorrect password. Please try again."

    except Exception as e:
        return False, f"Login failed: {str(e)}"


def get_user_profile(user_id):
    """Fetch full user profile from database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute(
            "SELECT UserID, Name, Email, CreatedAt FROM users WHERE UserID = ?",
            (user_id,)
        )
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "user_id":   row[0],
                "name":      row[1],
                "email":     row[2],
                "joined":    row[3],
            }
        return None
    except Exception:
        return None


def save_itinerary(user_id, destination, duration, plan_text):
    """Save a generated itinerary for a user."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute(
            """INSERT INTO itineraries (UserID, Destination, EndDate, GeneratedPlan)
               VALUES (?, ?, ?, ?)""",
            (user_id, destination, f"{duration} days", str(plan_text))
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_user_itineraries(user_id):
    """Retrieve all saved itineraries for a user."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute(
            """SELECT ItineraryID, Destination, EndDate, CreatedAt
               FROM itineraries WHERE UserID = ? ORDER BY CreatedAt DESC""",
            (user_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "id":          r[0],
                "destination": r[1],
                "duration":    r[2],
                "created_at":  r[3],
            }
            for r in rows
        ]
    except Exception:
        return []


def update_user_name(user_id, new_name):
    """Update the user's display name."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute("UPDATE users SET Name = ? WHERE UserID = ?", (new_name, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def delete_itinerary(itinerary_id, user_id):
    """Delete a saved itinerary (only if it belongs to the user)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        cur.execute(
            "DELETE FROM itineraries WHERE ItineraryID = ? AND UserID = ?",
            (itinerary_id, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False