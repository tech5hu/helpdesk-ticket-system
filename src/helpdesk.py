import csv  # let python read/write csv files
from pathlib import Path  # helps python safely locate files on any computer
from datetime import datetime  # for timestamps and submission time

# SET UP DATA FILE
# the file where all tickets are stored
DATA_FILE = Path(__file__).parent.parent / "data" / "helpdesk.csv"
LOG_FILE = Path(__file__).parent.parent / "logs" / "error.log"

# LOAD FUNCTION
def load_tickets():
    """Load tickets from CSV into memory, skip the corrupt rows, log any errors + return dict of valid tickets"""
    tickets = {}  # start with empty dictionary

    if not DATA_FILE.exists():
        print(f"No data file found at {DATA_FILE}. Starting with empty tickets.")
        return tickets

    # Making sure the log folder exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticket_id = row.get("ID", "").strip()

            # Check 1: ID must exist and has to be numeric
            if not ticket_id.isdigit():
                log_error(f"Invalid or missing ID: {ticket_id} - row skipped")
                continue

            # Check 2: Duplicate ID
            if ticket_id in tickets:
                log_error(f"Duplicate primary key {ticket_id} - row skipped")
                continue

            # Check 3: Required fields
            required_fields = ["Title", "Description", "Assignee", "Severity", "Status", "Category", "Submission Date", "Submission Time"]
            missing = [field for field in required_fields if not row.get(field)]
            if missing:
                log_error(f"Ticket {ticket_id} missing fields: {missing} - row skipped")
                continue

            # Check 4: Severity & Status validation
            if row["Severity"].lower() not in ["low", "medium", "high"]:
                log_error(f"Ticket {ticket_id} has invalid severity '{row['Severity']}' - row skipped")
                continue
            if row["Status"].lower() not in ["open", "in progress", "closed"]:
                log_error(f"Ticket {ticket_id} has invalid status '{row['Status']}' - row skipped")
                continue

            # All checks passed? THEN add to tickets
            tickets[ticket_id] = row  # SDE - keeps data structured for easy access
    return tickets

def log_error(message):
    """Write errors to log file with timestamp."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        # SDE - separates error logging from main logic
        # CS - keeps track of data issues safely for auditing
        # AI - log format is structured for future AI analysis

# SAVE FUNCTION
def save_tickets(tickets):
    """Save tickets from memory back to CSV"""
    fieldnames = ["ID", "Title", "Description", "Assignee", "Severity", "Status", "Category", "Submission Date", "Submission Time"]

    # Making sure the data folder exists
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # write column names
        for ticket in tickets.values():
            writer.writerow(ticket)
            # SDE - keeps CSV structured for maintainenance
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
    """Add a ticket with AI category prediction and ID validation"""
    # 1. Ensure unique numeric ID
    while True:
        ticket_id = input("Enter unique numeric ID: ").strip()
        if not ticket_id.isdigit():
            print("ID must be numeric. Try again.")
        elif ticket_id in tickets:
            print("ID already exists. Try a different one.")
        else:
            break

    # 2. Collect ticket info
    title = input("Enter ticket title: ").strip()
    description = input("Enter description: ").strip()
    assignee = input("Assign to (Olivia, Ryan, Jacob, Benjamin): ").strip()
    severity = input("Severity (High, Medium, Low): ").strip().title()
    status = input("Status (Open, In Progress, Closed): ").strip().title()

    # 3. AI predicts category
    category = predict_category(title).title()

    # 4. Add current date/time
    submission_date = datetime.now().strftime("%d/%m/%Y")
    submission_time = datetime.now().strftime("%H:%M:%S")

    # 5. Add to tickets
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

    # 6. Save
    save_tickets(tickets)
    print(f"Ticket added! Predicted category: {category}")
    # SDE - keeps ticket adding logic separate and structured
    # CS - ensures safe data storage
    # AI - immediately shows AI prediction to user

# VIEW TICKET DETAILS
def view_ticket_details(tickets):
    """Displays full details of a selected ticket. Implements input validation and safe lookup."""
    ticket_id = input("Please enter the Ticket ID: ").strip()
    # SDE - input separated into variable for cleaner logic
    # CS - .strip() prevents accidental spaces or injection inputs

    if not ticket_id.isdigit():
        print("Invalid Ticket ID. Must be numeric.")
        return
    # SDE - stops invalid data early
    # CS - prevents program errors or unexpected behavior

    # Safe lookup
    found_ticket = tickets.get(ticket_id)
    if not found_ticket:
        print("Ticket not found. Please try again.")
        return

    # Display ticket details clearly
    print("\n=== Ticket Details ===")
    for key, value in found_ticket.items():
        print(f"{key}: {value}")
    # SDE - readable display
    # CS - only shows safe info

    # AI FEATURE - highlight the high severity tickets
    if found_ticket['Severity'].lower() == "high":
        print("This is a HIGH severity ticket. Consider prioritising!")

    return found_ticket
    # SDE - return allows reusing this function
    # CS - avoids unnecessary global variable manipulation

# DELETE TICKET
def delete_ticket(tickets):
    """Delete a ticket by ID after confirmation"""
    ticket_id = input("Enter the Ticket ID to delete: ").strip()
    if not ticket_id.isdigit():
        print("Invalid Ticket ID. Must be numeric.")
        return

    found_ticket = tickets.get(ticket_id)
    if not found_ticket:
        print("Ticket not found. Please try again.")
        return

    # AI enhancement - warn if high severity
    if found_ticket['Severity'].lower() == "high":
        print("Warning: This is a HIGH severity ticket. Be careful before deleting!")

    confirm = input(f"Are you sure you want to delete ticket '{found_ticket['Title']}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return

    del tickets[ticket_id]
    save_tickets(tickets)
    print(f"Ticket {ticket_id} deleted successfully.")
    return found_ticket

# UPDATE TICKET
def update_ticket(tickets):
    """Amend an existing ticket safely with validation, logging and AI suggestions."""
    ticket_id = input("Enter the Ticket ID to update: ").strip()
    if not ticket_id.isdigit():
        print("Invalid Ticket ID. Must be numeric.")
        return

    ticket = tickets.get(ticket_id)
    if not ticket:
        print("Ticket not found.")
        return

    if ticket["Status"].lower() == "closed":
        print("Cannot update a closed ticket.")
        return

    print("\nCurrent Ticket Details:")
    for key, value in ticket.items():
        print(f"{key}: {value}")

    field = input(
        "\nEnter the field you want to update "
        "(Title, Description, Assignee, Severity, Status, Category): "
    ).strip().title()

    if field == "ID":
        print("Primary key cannot be modified.")
        return
    if field not in ticket:
        print("Invalid field selected.")
        return

    new_value = input(f"Enter new value for {field}: ").strip()
    if new_value == "":
        print("Field cannot be empty.")
        return

    # Validation for specific fields
    if field == "Severity":
        if new_value.lower() not in ["low", "medium", "high"]:
            print("Invalid severity. Must be Low, Medium, or High.")
            return
        new_value = new_value.title()

    if field == "Status":
        if new_value.lower() not in ["open", "in progress", "closed"]:
            print("Invalid status.")
            return
        new_value = new_value.title()

    # AI alerts
    if field == "Description":
        if "password" in new_value.lower() or "breach" in new_value.lower():
            print("AI Alert: This update may involve sensitive security information.")
    if field == "Severity" and new_value.lower() == "high":
        print("AI Suggestion: Consider escalating this ticket to senior support.")

    old_value = ticket[field]
    ticket[field] = new_value
    save_tickets(tickets)

    # Logging
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ticket {ticket_id}: Field '{field}' updated from '{old_value}' to '{new_value}'\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

    print("Ticket updated successfully. Changes recorded in the log.")
    return ticket