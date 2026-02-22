import csv # let python read/write csv files
from pathlib import Path # helps python safely locate files on any computer

# SET UP DATA FILE
# the file whee all tickets are stored
DATA_FILE = Path("data") / "helpdesk.csv"
# SDE - single variable for file path makes code easier to maintain
# CS - avoids hardcoding file paths everywhere, safer for data access
# AI - lets AI access data file for analysis

# LOAD FUNCTION
def load_tickets():
    """Load tickets from CSV into memory"""
    tickets = {}  # start with empty dictionary
    if DATA_FILE.exists():  # check the file actually exists first
        with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)  # read rows as dictionaries
            for row in reader:
                tickets[row["ID"]] = row  # store by ticket ID
                # SDE - keeps tickets easy to access by ID
                # CS - avoids manual string splitting, safer
                # AI - structured data is easy for AI analysis
    return tickets

# SAVE FUNCTION
def save_tickets(tickets):
    """Save tickets from memory back to CSV"""
    fieldnames = ["ID","Title","Description","Assignee","Severity","Status","Category","Submission Date","Submission Time"]
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # write column names
        for ticket in tickets.values():
            writer.writerow(ticket)
            # SDE - keeps CSV structured for maintainability
            # CS - prevents column misalignment so safer storage
            # AI - structured output allows AI to read and predict patterns            
# Load tickets when program starts
tickets = load_tickets()
# SDE - allows all functions to access tickets without reopening file
# CS - reduces risk of file errors
# AI - provides immediate data access for AI features