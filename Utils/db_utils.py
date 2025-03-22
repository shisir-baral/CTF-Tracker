import sqlite3
import logging
import os

# Build the path relative to the script's location.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up one folder and then go into the "database" folder
DB_DIR = os.path.join(BASE_DIR, "..", "database")
DB_DIR = os.path.abspath(DB_DIR)  # Normalize the path

os.makedirs(DB_DIR, exist_ok=True)  # Ensure the folder exists

# Define the full path to the database file
DB_PATH = os.path.join(DB_DIR, "ctf_tracker.db")
def init_db(db_path=DB_PATH):
    """
    Initialize the SQLite database with tables for users, CTFs, and contributions.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table for user info if it doesn't exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            NetID TEXT PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)
    
    # Create table for CTF events if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ctf_events (
            ctf_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ctf_name TEXT NOT NULL UNIQUE,
            ctftime_score REAL NOT NULL
        )
    """)
    
    # Create table for contributions if it doesn't exist.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            ctf_id INTEGER NOT NULL,
            ctf_score REAL NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username),
            FOREIGN KEY(ctf_id) REFERENCES ctf_events(ctf_id)
        )
    """)
    conn.commit()
    return conn

def add_user(conn, username, NetID):
    """
    Add a new user to the database.
    """
    try:
        conn.execute("INSERT INTO users (NetID, username) VALUES (?, ?)", (NetID, username))
        conn.commit()
        logging.info("Added new user: %s", NetID)
        return True
    except sqlite3.IntegrityError:
        logging.info("User already exists: %s", NetID)
        return False

def add_ctf_event(conn, ctf_name, ctftime_score):
    """
    Add a new CTF event to the database.
    """
    try:
        conn.execute("INSERT INTO ctf_events (ctf_name, ctftime_score) VALUES (?, ?)", 
                   (ctf_name, ctftime_score))
        conn.commit()
        logging.info("Added new CTF event: %s", ctf_name)
        return True
    except sqlite3.IntegrityError:
        logging.info("CTF event already exists: %s", ctf_name)
        return False

def get_ctf_id(conn, ctf_name):
    """
    Get the CTF ID for a given CTF name.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT ctf_id FROM ctf_events WHERE ctf_name = ?", (ctf_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def add_contribution(conn, username, ctf_name, ctf_score):
    """
    Add a new contribution record for a given username and CTF.
    """
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        return False, "User not found"
    
    # Get the CTF ID
    ctf_id = get_ctf_id(conn, ctf_name)
    if ctf_id is None:
        return False, "CTF event not found"
    
    # Add the contribution
    try:
        conn.execute(
            "INSERT INTO contributions (username, ctf_id, ctf_score) VALUES (?, ?, ?)",
            (username, ctf_id, ctf_score)
        )
        conn.commit()
        logging.info("Added contribution for user: %s in CTF: %s", username, ctf_name)
        return True, "Contribution added successfully"
    except Exception as e:
        return False, f"Error adding contribution: {str(e)}"

def query_top_contributors(conn):
    """
    Query the database to find which users contributed the most.
    Here, total contribution is calculated as the sum of (ctf_score * ctftime_score).
    """
    query = """
        SELECT u.username, u.NetID, SUM(c.ctf_score * e.ctftime_score) AS total_contribution
        FROM contributions c
        JOIN users u ON c.username = u.username
        JOIN ctf_events e ON c.ctf_id = e.ctf_id
        GROUP BY c.username
        ORDER BY total_contribution DESC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_all_contributions(conn):
    """
    Get all contributions with additional detail.
    """
    query = """
        SELECT c.id, u.username, u.NetID, e.ctf_name, c.ctf_score, e.ctftime_score, 
               (c.ctf_score * e.ctftime_score) AS contribution_value
        FROM contributions c
        JOIN users u ON c.username = u.username
        JOIN ctf_events e ON c.ctf_id = e.ctf_id
        ORDER BY c.id DESC
    """
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_all_users(conn):
    """
    Get all registered users.
    """
    query = "SELECT NetID, username FROM users ORDER BY NetID"
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def get_all_ctf_events(conn):
    """
    Get all CTF events.
    """
    query = "SELECT ctf_id, ctf_name, ctftime_score FROM ctf_events ORDER BY ctf_name"
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def search_contributions(conn, username=None, netid=None, ctf_name=None):
    """
    Search for contributions based on criteria.
    """
    query = """
        SELECT c.id, u.username, u.NetID, e.ctf_name, c.ctf_score, e.ctftime_score,
               (c.ctf_score * e.ctftime_score) AS contribution_value
        FROM contributions c
        JOIN users u ON c.username = u.username
        JOIN ctf_events e ON c.ctf_id = e.ctf_id
        WHERE 1=1
    """
    params = []
    
    if username:
        query += " AND u.username LIKE ?"
        params.append(f"%{username}%")
    
    if netid:
        query += " AND u.NetID LIKE ?"
        params.append(f"%{netid}%")
    
    if ctf_name:
        query += " AND e.ctf_name LIKE ?"
        params.append(f"%{ctf_name}%")
    
    query += " ORDER BY c.id DESC"
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    return results

def delete_contribution(conn, contribution_id):
    """
    Delete a contribution by its ID.
    """
    try:
        conn.execute("DELETE FROM contributions WHERE id = ?", (contribution_id,))
        conn.commit()
        return True
    except Exception as e:
        logging.error("Error deleting contribution: %s", str(e))
        return False

def interactive_entry(conn):
    """
    Loop to interactively collect input for new contributions.
    """
    print("First, let's check if we need to add a CTF event:")
    ctf_name = input("Enter CTF name: ").strip()
    
    # Check if CTF exists
    cursor = conn.cursor()
    cursor.execute("SELECT ctf_id FROM ctf_events WHERE ctf_name = ?", (ctf_name,))
    ctf_result = cursor.fetchone()
    
    if ctf_result is None:
        try:
            ctftime_score = float(input("New CTF event. Enter CTFtime score (difficulty): ").strip())
            add_ctf_event(conn, ctf_name, ctftime_score)
        except ValueError:
            print("Invalid input. Please enter a numeric value for the score.")
            return
    
    # Now add contribution
    while True:
        username = input("Enter username (or 'q' to quit): ").strip()
        if username.lower() == 'q':
            break
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is None:
            netid = input(f"Username '{username}' not found. Please enter the NetID: ")
            add_user(conn, username, netid)
        
        try:
            ctf_score = float(input("Enter CTF score for this event: ").strip())
        except ValueError:
            print("Invalid input. Please enter a numeric value for the score.")
            continue
            
        success, message = add_contribution(conn, username, ctf_name, ctf_score)
        if success:
            print(message)
        else:
            print(f"Error: {message}")
