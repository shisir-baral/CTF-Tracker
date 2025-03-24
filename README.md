The **CTF Contribution Tracker** is a Python application designed to track contributions to Capture The Flag (CTF) events. It supports both a graphical user interface (GUI) using Tkinter and a command-line interface (CLI) for managing users, CTF events, and individual contributions. The application uses SQLite to store data persistently and calculates total contributions based on CTF scores and event difficulty (CTFtime scores).

## Features

- **User Management**: Add and view registered users with their usernames and NetIDs.
- **CTF Event Management**: Add and view CTF events with names and CTFtime scores (difficulty ratings).
- **Contribution Tracking**: Record contributions per user and CTF event, with scores weighted by event difficulty.
- **GUI Interface**: A tabbed Tkinter interface for adding, viewing, and deleting entries.
- **CLI Interface**: Options to add contributions or query top contributors via the command line.
- **Search and Delete**: Search contributions by username, NetID, or CTF name, and delete specific entries.
- **Logging**: Logs application events to both a file (`app.log`) and the terminal for debugging and tracking.

## Requirements

- Python 3.x
- Modules:
  - `tkinter` (usually included with Python)
  - `sqlite3` (included with Python)
  - `argparse` (included with Python)
  - `logging` (included with Python)
  - `os` (included with Python)

No external libraries are required beyond the Python standard library.

## Installation

1. **Clone or Download the Repository**:
   - Clone this repository or download the source code to your local machine.

2. **Directory Structure**:
   Ensure your project directory looks like this:
```
   CTF_Contribution_Tracker/
   ├── main.py
   ├── Utils/
   │   ├── db_utils.py
   │   └── gui_utils.py
   ├── logs/           (created automatically on first run)
   └── database/       (created automatically on first run)
```

3. **Run the Application**:
- Navigate to the project directory in your terminal.
- Run the main script:  
  ```bash
  python3 main.py
  ```

## Usage

Graphical User Interface (GUI)
The GUI provides a tabbed interface with the following options:

    Add Contribution: Add a contribution by selecting a username, CTF name, and entering a score.
    Add User: Register a new user with a username and NetID.
    Add CTF: Add a new CTF event with a name and CTFtime score.
    View Contributions: Display all contributions with details (ID, username, NetID, CTF name, scores, total value).
    View Users: List all registered users.
    View CTFs: List all CTF events.
    Delete Entries: Search for contributions and delete specific entries.

Database

    The application creates a SQLite database (ctf_tracker.db) in the database/ folder.
    Tables:
        users: Stores NetID and username.
        ctf_events: Stores CTF event details (ID, name, CTFtime score).
        contributions: Stores contribution records (ID, username, CTF ID, score).

Example Workflow

    Add a User:
        Go to "Add User," enter username: alice, NetID: abc123, and submit.
    Add a CTF Event:
        Go to "Add CTF," enter CTF Name: ExampleCTF, CTFtime Score: 25.0, and submit.
    Add a Contribution:
        Go to "Add Contribution," select alice, ExampleCTF, enter CTF Score: 10.0, and submit.

Logging

    Logs are saved to logs/app.log and printed to the terminal.
    Includes info like user additions, CTF events, and contribution records.

Future Improvements

    Add export functionality (e.g., CSV export of contributions).
    Implement user authentication for secure access.
    Enhance the GUI with sorting and filtering options in tables.
    Add a configuration file for customizable settings (e.g., database path).

Contributing
Feel free to fork this repository, submit issues, or create pull requests with improvements!
License
This project is open-source and available under the MIT License (LICENSE).

### Notes
- **File Placement**: Save this as `README.md` in the root of your project directory.
- **Customization**: Adjust the "Future Improvements" section based on your plans, and update the "License" section if you have a specific license in mind.
- **Assumptions**: I assumed the code is split into `main.py`, `db_utils.py`, and `gui_utils.py` under a `Utils/` folder based on your imports. Adjust the directory structure in the README if this isn’t correct.
