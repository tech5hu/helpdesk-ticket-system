from pathlib import Path
from datetime import datetime
import json
from json import JSONDecodeError
import csv

# defining where ticket data and logs are stored
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "helpdesk.csv"
LOG_FILE = BASE_DIR / "logs" / "error.log"

print("DATA FILE PATH:", DATA_FILE)


def load_tickets():
    """Load tickets from the CSV file into memory"""
    tickets = {}  # storing tickets in a dictionary for fast lookup by ID

    if not DATA_FILE.exists():
        print(f"No data file found at {DATA_FILE}. Starting empty.")
        return tickets  # CS - fail safely if data file missing

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # CS - ensure logging directory exists

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticket_id = row.get("ID", "").strip()

            if not ticket_id.isdigit():
                log_error(f"Invalid or missing ID: {ticket_id} - row skipped")
                continue  # CS - enforce numeric primary key

            if ticket_id in tickets:
                log_error(f"Duplicate ID {ticket_id} - row skipped")
                continue  # CS - prevent duplicate primary keys

            required_fields = [
                "Title", "Description", "Assignee",
                "Severity", "Status", "Category",
                "Submission DateTime"
            ]

            missing = [field for field in required_fields if not row.get(field)]
            if missing:
                log_error(f"Ticket {ticket_id} missing fields: {missing} - row skipped")
                continue  # CS - reject incomplete records

            if row["Severity"].lower() not in ["low", "medium", "high"]:
                log_error(f"Ticket {ticket_id} has invalid severity - row skipped")
                continue  # CS - enforce allowed values

            if row["Status"].lower() not in ["open", "in progress", "closed"]:
                log_error(f"Ticket {ticket_id} has invalid status - row skipped")
                continue  # CS - enforce allowed values

            try:
                row["Comments"] = json.loads(row.get("Comments", "[]"))
            except JSONDecodeError:
                row["Comments"] = []  # CS - prevent corrupted comment data from crashing system

            tickets[ticket_id] = row

    return tickets


def log_error(message):
    """Write errors to the log file"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")
        # CS - maintain timestamped audit trail


def save_tickets(tickets):
    """Save all tickets back to the CSV file"""
    fieldnames = [
        "ID", "Title", "Description", "Assignee",
        "Severity", "Status", "Category",
        "Submission DateTime", "Comments"
    ]

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ticket in tickets.values():
            ticket_copy = ticket.copy()
            ticket_copy["Comments"] = json.dumps(ticket_copy.get("Comments", []))
            writer.writerow(ticket_copy)
    # CS - ensures structured, consistent data persistence


tickets = load_tickets()
# CS - load once to reduce repeated file access


def predict_category(title):
    """Guess ticket category using keywords"""
    title_lower = title.lower()

    if any(word in title_lower for word in ["password", "login", "account"]):
        return "Security"
    elif any(word in title_lower for word in ["printer", "hardware", "microphone", "camera"]):
        return "Hardware"
    elif any(word in title_lower for word in ["vpn", "wifi", "network"]):
        return "Network"
    return "Software"


def add_ticket():
    """Add a new ticket safely"""
    while True:
        ticket_id = input("Enter unique numeric ID: ").strip()

        if not ticket_id.isdigit():
            print("ID must be numeric.")
        elif ticket_id in tickets:
            print("ID already exists.")
        else:
            break  # CS - enforce unique numeric identifier

    title = input("Enter ticket title: ").strip()
    description = input("Enter description: ").strip()
    assignee = input("Assign to (Olivia, Ryan, Jacob, Benjamin): ").strip()
    severity = input("Severity (High, Medium, Low): ").strip().title()
    status = input("Status (Open, In Progress, Closed): ").strip().title()

    category = predict_category(title)
    submission_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    tickets[ticket_id] = {
        "ID": ticket_id,
        "Title": title,
        "Description": description,
        "Assignee": assignee,
        "Severity": severity,
        "Status": status,
        "Category": category,
        "Submission DateTime": submission_datetime,
        "Comments": []
    }

    save_tickets(tickets)
    print(f"Ticket added! Predicted category: {category}")


def update_ticket(tickets):
    """Update a ticket safely"""
    ticket_id = input("Enter the Ticket ID to update: ").strip()

    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        return

    ticket = tickets.get(ticket_id)
    if not ticket:
        print("Ticket not found.")
        return

    if ticket["Status"].lower() == "closed":
        print("Cannot update a closed ticket.")
        return  # CS - protect integrity of closed records

    field = input(
        "Field to update (Title, Description, Assignee, Severity, Status, Category): "
    ).strip().title()

    if field == "ID":
        print("ID cannot be changed.")
        return  # CS - protect primary key

    if field not in ticket:
        print("Invalid field.")
        return

    new_value = input(f"Enter new value for {field}: ").strip()
    if not new_value:
        print("Field cannot be empty.")
        return

    old_value = ticket[field]
    ticket[field] = new_value
    save_tickets(tickets)

    log_error(
        f"Ticket {ticket_id}: {field} changed from '{old_value}' to '{new_value}'"
    )
    # CS - maintain change audit trail

    print("Ticket updated successfully.")