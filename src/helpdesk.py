import csv  # SDE - lets the program read and write CSV files
from pathlib import Path  # SDE - helps find files safely on any computer
from datetime import datetime  # SDE - lets us record dates and times

# SDE - set where the data and log files are stored
DATA_FILE = Path(__file__).parent.parent / "data" / "helpdesk.csv"
LOG_FILE = Path(__file__).parent.parent / "logs" / "error.log"


def load_tickets():
    """Load tickets from the CSV file into memory"""
    tickets = {}  # SDE - use a dictionary to store tickets by ID

    if not DATA_FILE.exists():
        print(f"No data file found at {DATA_FILE}. Starting empty.")
        return tickets  # CS - stop the program crashing if file is missing

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # CS - make sure the log folder exists

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # SDE - read each row as a dictionary
        for row in reader:
            ticket_id = row.get("ID", "").strip()  # CS - safely get the ID and remove spaces

            if not ticket_id.isdigit():
                log_error(f"Invalid or missing ID: {ticket_id} - row skipped")  # CS - skip bad IDs
                continue

            if ticket_id in tickets:
                log_error(f"Duplicate ID {ticket_id} - row skipped")  # CS - stop two tickets having same ID
                continue

            required_fields = ["Title", "Description", "Assignee", "Severity", "Status", "Category", "Submission Date", "Submission Time"]
            missing = [field for field in required_fields if not row.get(field)]
            if missing:
                log_error(f"Ticket {ticket_id} missing fields: {missing} - row skipped")  # CS - skip incomplete rows
                continue

            if row["Severity"].lower() not in ["low", "medium", "high"]:
                log_error(f"Ticket {ticket_id} has invalid severity - row skipped")  # CS - only allow set severity values
                continue

            if row["Status"].lower() not in ["open", "in progress", "closed"]:
                log_error(f"Ticket {ticket_id} has invalid status - row skipped")  # CS - only allow set status values
                continue

            tickets[ticket_id] = row  # SDE - save the ticket using its ID so we can find it later

    return tickets  # SDE - return all valid tickets


def log_error(message):
    """Write errors to the log file"""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")  # SDE - add time to each log entry
        # CS - keep a record of problems for review
        # AI - logs could be analysed later to spot patterns


def save_tickets(tickets):
    """Save all tickets back to the CSV file"""
    fieldnames = ["ID", "Title", "Description", "Assignee", "Severity", "Status", "Category", "Submission Date", "Submission Time"]

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  # CS - make sure the data folder exists

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)  # SDE - keep columns organised/aligned
        writer.writeheader()  # SDE - write the column titles first
        for ticket in tickets.values():
            writer.writerow(ticket)  # SDE - write each ticket as a row
            # CS - keeps the file neat and prevents broken columns
            # AI - clean data makes future analysis easier


tickets = load_tickets()  # SDE - load tickets once when the program starts
# CS - reduces repeated file access
# AI - makes data ready for smart features


def predict_category(title):
    """Guess ticket category using keywords"""
    title_lower = title.lower()  # AI - make text lowercase for easier checking

    if any(word in title_lower for word in ["password", "login", "account"]):
        return "Security"  # AI - detect security words
    elif any(word in title_lower for word in ["printer", "hardware", "microphone", "camera"]):
        return "Hardware"  # AI - detect device issues
    elif any(word in title_lower for word in ["vpn", "wifi", "network"]):
        return "Network"  # AI - detect connection problems
    else:
        return "Software"  # AI - default if nothing matches


def add_ticket():
    """Add a new ticket safely"""

    while True:
        ticket_id = input("Enter unique numeric ID: ").strip()  # CS - clean user input
        if not ticket_id.isdigit():
            print("ID must be numeric.")  # CS - stop letters in ID
        elif ticket_id in tickets:
            print("ID already exists.")  # CS - stop duplicate IDs
        else:
            break

    title = input("Enter ticket title: ").strip()  # SDE - collect ticket details
    description = input("Enter description: ").strip()
    assignee = input("Assign to (Olivia, Ryan, Jacob, Benjamin): ").strip()
    severity = input("Severity (High, Medium, Low): ").strip().title()
    status = input("Status (Open, In Progress, Closed): ").strip().title()

    category = predict_category(title).title()  # AI - automatically choose a category

    submission_date = datetime.now().strftime("%d/%m/%Y")  # SDE - record today’s date
    submission_time = datetime.now().strftime("%H:%M:%S")  # SDE - record current time

    tickets[ticket_id] = {  # SDE - add the new ticket to memory
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

    save_tickets(tickets)  # SDE - save changes so they are not lost
    print(f"Ticket added! Predicted category: {category}")  # AI - show AI result to user


def view_ticket_details(tickets):
    """Show full details of a ticket"""

    ticket_id = input("Enter the Ticket ID: ").strip()  # CS - clean input

    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")  # CS - stop bad input
        return

    found_ticket = tickets.get(ticket_id)  # SDE - safely look up ticket
    if not found_ticket:
        print("Ticket not found.")  # CS - avoid errors if ID does not exist
        return

    print("\n=== Ticket Details ===")  # SDE - clear heading
    for key, value in found_ticket.items():
        print(f"{key}: {value}")  # SDE - display all fields clearly

    if found_ticket['Severity'].lower() == "high":
        print("This is a HIGH severity ticket.")  # AI - highlight important tickets

    return found_ticket  # SDE - return the ticket if needed elsewhere


def delete_ticket(tickets):
    """Delete a ticket safely"""

    ticket_id = input("Enter the Ticket ID to delete: ").strip()  # CS - clean input
    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        return

    found_ticket = tickets.get(ticket_id)  # SDE - find ticket safely
    if not found_ticket:
        print("Ticket not found.")
        return

    if found_ticket['Severity'].lower() == "high":
        print("Warning: This is a HIGH severity ticket.")  # AI - warn before deleting important ticket

    confirm = input(f"Delete ticket '{found_ticket['Title']}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")  # CS - stop accidental deletion
        return

    del tickets[ticket_id]  # SDE - remove from memory
    save_tickets(tickets)  # SDE - save the change
    print("Ticket deleted successfully.")


def update_ticket(tickets):
    """Update a ticket safely"""

    ticket_id = input("Enter the Ticket ID to update: ").strip()  # CS - clean input
    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        return

    ticket = tickets.get(ticket_id)  # SDE - find the ticket safely
    if not ticket:
        print("Ticket not found.")
        return

    if ticket["Status"].lower() == "closed":
        print("Cannot update a closed ticket.")  # CS - protect finished tickets
        return

    print("\nCurrent Ticket Details:")
    for key, value in ticket.items():
        print(f"{key}: {value}")  # SDE - show current values

    field = input("Field to update (Title, Description, Assignee, Severity, Status, Category): ").strip().title()

    if field == "ID":
        print("ID cannot be changed.")  # CS - protect ticket ID
        return

    if field not in ticket:
        print("Invalid field.")
        return

    new_value = input(f"Enter new value for {field}: ").strip()
    if new_value == "":
        print("Field cannot be empty.")  # CS - stop blank values
        return

    if field == "Severity" and new_value.lower() not in ["low", "medium", "high"]:
        print("Invalid severity.")
        return

    if field == "Status" and new_value.lower() not in ["open", "in progress", "closed"]:
        print("Invalid status.")
        return

    if field == "Description" and ("password" in new_value.lower() or "breach" in new_value.lower()):
        print("AI Alert: This may involve security information.")  # AI - warn about sensitive words

    if field == "Severity" and new_value.lower() == "high":
        print("AI Suggestion: Consider escalating this ticket.")  # AI - suggest action for high severity

    old_value = ticket[field]  # SDE - remember old value for logging
    ticket[field] = new_value  # SDE - update the field
    save_tickets(tickets)  # SDE - save the change

    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ticket {ticket_id}: {field} changed from '{old_value}' to '{new_value}'\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # CS - ensure log folder exists
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)  # CS - record what was changed

    print("Ticket updated successfully.")