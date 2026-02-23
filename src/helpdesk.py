import csv # let python read/write csv files
from pathlib import Path # helps python safely locate files on any computer

# SET UP DATA FILE
# the file whee all tickets are stored
DATA_FILE = Path(__file__).parent.parent / "data" / "helpdesk.csv"
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

# AI FEATURE
def predict_category(title):
    """Predict ticket category from keywords"""
    title_lower = title.lower()  # lowercase text for simple checks

    if any(word in title_lower for word in ["password", "login", "account"]):
        return "Security"
    elif any(word in title_lower for word in ["printer", "hardware", "microphone", "camera"]):
        return "Hardware"
    elif any(word in title_lower for word in ["vpn", "wifi", "network"]):
        return "Network"
    else:
        return "Software"
    # AI benefit - reduces human error and speeds categorisation
    # SDE - keeps prediction logic separate for easier improvement
    # CS - avoids hardcoding categories throughout the program

# ADD TICKET FUNCTION
def add_ticket():
    """Add a ticket with AI category prediction"""
    ticket_id = input("Enter unique numeric ID: ")
    title = input("Enter ticket title: ")
    description = input("Enter description: ")
    assignee = input("Assign to (Olivia, Ryan, Jacob, Benjamin): ")
    severity = input("Severity (High, Medium, Low): ")
    status = input("Status (Open, In Progress, Closed): ")

    category = predict_category(title)  # AI predicts category

    from datetime import datetime
    submission_date = datetime.now().strftime("%d/%m/%Y")
    submission_time = datetime.now().strftime("%H:%M:%S")

    tickets[ticket_id] = {
        "ID": ticket_id,
        "Title": title,
        "Description": description,
        "Assignee": assignee,
        "Severity": severity,
        "Status": status,
        "Category": category,
        "Submission Date": submission_date,
        "Submission Time": submission_time
    }
    save_tickets(tickets)  # Save tickets back to csv
    print(f"Ticket added! Predicted category: {category}")
    # SDE - keeps ticket adding logic separate and structured
    # CS - ensures safe data storage
    # AI - immediately shows AI prediction to user

# VIEW TICKET DETAILS
def view_ticket_details(tickets):
    """Displays full details of a selected ticket.
       Implements input validation and safe lookup.
    """
    
    # 1. Ask user for ticket ID
    ticket_id = input("Please enter the Ticket ID: ").strip()
    # SDE - input separated into variable for cleaner logic
    # CS - .strip() prevents accidental spaces or injection inputs

    # 2. Validate ticket ID format
    if not ticket_id.isdigit():
        print("Invalid Ticket ID. Must be numeric.")
        return
    # SDE - stops invalid data early
    # CS - prevents program errors or unexpected behavior

    # 3. Search for the ticket safely
    found_ticket = None
    for ticket in tickets.values():  # values() ensures access to ticket dictionaries
        if ticket["ID"] == ticket_id:  # matches against primary key
            found_ticket = ticket
            break
    if found_ticket is None:
        print("Ticket not found. Please try again.")
        return
    # SDE - search logic separated, easier to maintain
    # CS - avoids showing info for invalid IDs

    # 4. Display formatted details clearly
    print("\n=== Ticket Details ===")
    print(f"ID: {found_ticket['ID']}")
    print(f"Title: {found_ticket['Title']}")
    print(f"Description: {found_ticket['Description']}")
    print(f"Assignee: {found_ticket['Assignee']}")
    print(f"Severity: {found_ticket['Severity']}")
    print(f"Status: {found_ticket['Status']}")
    print(f"Category: {found_ticket['Category']}")
    print(f"Submission Date: {found_ticket['Submission Date']}")
    print(f"Submission Time: {found_ticket['Submission Time']}")
    # SDE - each field printed clearly for readability
    # CS - only displays relevant fields safely

    # AI FEATURE - highlight the high severity tickets
    if found_ticket['Severity'].lower() == "high":
        print("This is a HIGH severity ticket. Consider prioritising!")

    # 5. Return ticket safely for further actions
    return found_ticket
    # SDE - return allows reusing this function for multiple workflows
    # CS - avoids unnecessary global variable manipulation
    