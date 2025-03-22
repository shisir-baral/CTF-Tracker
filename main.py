#!/usr/bin/env python3
import argparse
import logging
import tkinter as tk
from Utils import gui_utils
from Utils import db_utils
import os

# Determine the base directory (where main.py is located) and create a logs folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure the logs folder exists
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Setup logging for the application.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # This will also print logs to terminal.
    ]
)
def main():
    parser = argparse.ArgumentParser(description="CTF Contribution Tracker")
    parser.add_argument(
        "--mode",
        choices=["gui", "add", "query"],
        default="gui",
        help="Mode: 'gui' for graphical interface; 'add' to add new contributions via CLI; 'query' to view top contributors via CLI."
    )
    args = parser.parse_args()

    conn = db_utils.init_db()

    if args.mode == "gui":
        root = tk.Tk()
        app = gui_utils.CTFTrackerGUI(root)
        root.mainloop()
        conn.close()
    elif args.mode == "add":
        db_utils.interactive_entry(conn)
        conn.close()
    elif args.mode == "query":
        results = gui_utils.query_top_contributors(conn)
        if results:
            print("Top Contributors:")
            for username, netid, total in results:
                print(f"Username: {username}, NetID: {netid}, Total Contribution: {total:.2f}")
        else:
            print("No contributions found.")
        conn.close()

if __name__ == '__main__':
    main()