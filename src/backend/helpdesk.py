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
        return tickets  # CS - avoid crashing if the file does not exist

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # CS - ensure the log folder exists

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # reading each row as a dictionary for clarity
        for row in reader:
            ticket_id = row.get("ID", "").strip()  # CS - clean input to avoid errors

            if not ticket_id.isdigit():
                log_error(f"Invalid or missing ID: {ticket_id} - row skipped")  # CS - skip invalid IDs
                continue

            if ticket_id in tickets:
                log_error(f"Duplicate ID {ticket_id} - row skipped")  # CS - prevent duplicate tickets
                continue

            # checking required fields exist
            required_fields = ["Title", "Description", "Assignee", "Severity", "Status", "Category", "Submission DateTime"]
            missing = [field for field in required_fields if not row.get(field)]
            if missing:
                log_error(f"Ticket {ticket_id} missing fields: {missing} - row skipped")  # CS - skip incomplete tickets
                continue

            if row["Severity"].lower() not in ["low", "medium", "high"]:
                log_error(f"Ticket {ticket_id} has invalid severity - row skipped")  # CS - ensure valid severity
                continue

            if row["Status"].lower() not in ["open", "in progress", "closed"]:
                log_error(f"Ticket {ticket_id} has invalid status - row skipped")  # CS - ensure valid status
                continue

            try:
                row["Comments"] = json.loads(row.get("Comments", "[]"))
            except JSONDecodeError:
                row["Comments"] = []


            tickets[ticket_id] = row  # saving the ticket using its ID

    return tickets 


def log_error(message):
    """Write errors to the log file"""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")  
        # include timestamp for clarity
        # CS - keeps a record of problems for review


def save_tickets(tickets):
    """Save all tickets back to the CSV file"""
    fieldnames = ["ID", "Title", "Description", "Assignee", "Severity", "Status", "Category", "Submission DateTime", "Comments"]

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  # CS - ensure the data folder exists

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames) 
        writer.writeheader()  # writing the column titles first
        for ticket in tickets.values():
            ticket_copy = ticket.copy()
            ticket_copy["Comments"] = json.dumps(ticket_copy.get("Comments", []))
            writer.writerow(ticket_copy)
            # CS - ensures the file stays consistent and readable


tickets = load_tickets()
# CS - reduces repeated file access

def predict_category(title):
    """Guess ticket category using keywords"""
    title_lower = title.lower()  

    if any(word in title_lower for word in ["password", "login", "account"]):
        return "Security"  
    elif any(word in title_lower for word in ["printer", "hardware", "microphone", "camera"]):
        return "Hardware"  
    elif any(word in title_lower for word in ["vpn", "wifi", "network"]):
        return "Network"  
    else:
        return "Software"  

def add_ticket():
    """Add a new ticket safely"""

    while True:
        ticket_id = input("Enter unique numeric ID: ").strip()  # CS - clean input
        if not ticket_id.isdigit():
            print("ID must be numeric.")  # CS - prevent invalid ID
        elif ticket_id in tickets:
            print("ID already exists.")  # CS - prevent duplicates
        else:
            break

    title = input("Enter ticket title: ").strip() 
    description = input("Enter description: ").strip()
    assignee = input("Assign to (Olivia, Ryan, Jacob, Benjamin): ").strip()
    severity = input("Severity (High, Medium, Low): ").strip().title()
    status = input("Status (Open, In Progress, Closed): ").strip().title()

    category = predict_category(title).title() 

    submission_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    tickets[ticket_id] = {  # adding ticket to memory
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


def view_ticket_details(tickets):
    """Show full details of a ticket"""

    ticket_id = input("Enter the Ticket ID: ").strip()  # CS - clean input

    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")  # CS - prevent invalid input
        return

    found_ticket = tickets.get(ticket_id) 
    if not found_ticket:
        print("Ticket not found.")  # CS - avoid errors
        return

    print("\n=== Ticket Details ===")  
    for key, value in found_ticket.items():
        if key == "Comments":
            print(f"{key}:")
            for comment in value:
                print(f" - {comment}") 
        else:
            print(f"{key}: {value}")  

    if found_ticket['Severity'].lower() == "high":
        print("This is a HIGH severity ticket.") 

    return found_ticket  


def delete_ticket(tickets):
    """Delete a ticket safely"""

    ticket_id = input("Enter the Ticket ID to delete: ").strip()  # CS - clean input
    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        return

    found_ticket = tickets.get(ticket_id) 
    if not found_ticket:
        print("Ticket not found.")
        return

    if found_ticket['Severity'].lower() == "high":
        print("Warning: This is a HIGH severity ticket.")  

    confirm = input(f"Delete ticket '{found_ticket['Title']}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")  # CS - prevent accidental deletion
        return

    del tickets[ticket_id] 
    save_tickets(tickets) 
    print("Ticket deleted successfully.")


def update_ticket(tickets):
    """Update a ticket safely"""

    ticket_id = input("Enter the Ticket ID to update: ").strip()  # CS - clean input
    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        return

    ticket = tickets.get(ticket_id)  
    if not ticket:
        print("Ticket not found.")
        return

    if ticket["Status"].lower() == "closed":
        print("Cannot update a closed ticket.")  # CS - protect finished tickets
        return

    print("\nCurrent Ticket Details:")
    for key, value in ticket.items():
        print(f"{key}: {value}")  

    field = input("Field to update (Title, Description, Assignee, Severity, Status, Category): ").strip().title()

    if field == "ID":
        print("ID cannot be changed.")  # CS - prevent altering primary identifier
        return

    if field not in ticket:
        print("Invalid field.")
        return

    new_value = input(f"Enter new value for {field}: ").strip()
    if new_value == "":
        print("Field cannot be empty.")  # CS - prevent blank updates
        return

    if field == "Severity" and new_value.lower() not in ["low", "medium", "high"]:
        print("Invalid severity.")
        return

    if field == "Status" and new_value.lower() not in ["open", "in progress", "closed"]:
        print("Invalid status.")
        return

    if field == "Description" and ("password" in new_value.lower() or "breach" in new_value.lower()):
        print("AI Alert: This may involve security information.") 

    if field == "Severity" and new_value.lower() == "high":
        print("AI Suggestion: Consider escalating this ticket.") 

    old_value = ticket[field]  # remembering old value for tracking
    ticket[field] = new_value  # updating the field
    save_tickets(tickets)  # keeping the changes

    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ticket {ticket_id}: {field} changed from '{old_value}' to '{new_value}'\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # CS - ensure log folder exists
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)  # CS - record changes for accountability

    print("Ticket updated successfully.")

def add_comment(tickets):
    """Add a comment to a ticket"""

    ticket_id = input("Enter Ticket ID to comment on: ").strip()

    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        return

    ticket = tickets.get(ticket_id)
    if not ticket:
        print("Ticket not found.")
        return

    comment_text = input("Enter your comment: ").strip()
    if not comment_text:
        print("Comment cannot be empty.")
        return

    if any(word in comment_text.lower() for word in ["password", "confidential", "breach"]):
        print("AI Warning: Comment may contain sensitive information.")

    # store comment as a dict (like in web version)
    comment_dict = {
        "Author": "CLI User",
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Content": comment_text
    }

    ticket.setdefault("Comments", []).append(comment_dict)  # append dict, not string

    save_tickets(tickets)  # save changes
    print("Comment added successfully.")
    
def close_ticket(tickets):
    """Close a ticket safely"""

    ticket_id = input("Enter Ticket ID to close: ").strip()  
    # CS - removes extra spaces to reduce errors

    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        # CS - only allows valid number IDs
        return

    ticket = tickets.get(ticket_id)  

    if not ticket:
        print("Ticket not found.")
        # CS - stops the program if the ticket does not exist
        return

    if ticket["Status"].lower() == "closed":
        print("Ticket is already closed.")  

        return  

    ticket["Status"] = "Closed"  

    save_tickets(tickets)  

    print(f"Ticket {ticket_id} closed successfully.")

def escalate_ticket(tickets):
    """Escalate a ticket to another assignee"""

    ticket_id = input("Enter Ticket ID to escalate: ").strip()  
    # CS - cleans the input to prevent mistakes

    if not ticket_id.isdigit():
        print("Invalid Ticket ID.")
        # CS - ensures valid ID format
        return

    ticket = tickets.get(ticket_id)  

    if not ticket:
        print("Ticket not found.")
        # CS - prevents changes to non existent tickets
        return

    if ticket["Status"].lower() == "closed":
        print("Cannot escalate a closed ticket.")  
        # CS - prevents changes to completed tickets
        return  

    new_assignee = input("Enter new assignee: ").strip()

    if ticket["Severity"].lower() == "high":
        print("AI Suggestion: High severity tickets should be assigned to senior staff.")

    old_assignee = ticket["Assignee"]

    ticket["Assignee"] = new_assignee
    ticket["Severity"] = "High"  
    ticket["Status"] = "In Progress"
    # updating related fields together to keep data consistent

    save_tickets(tickets)

    log_error(f"Ticket {ticket_id} escalated from {old_assignee} to {new_assignee}")
    # CS - records the change for accountability and tracking

    print(f"Ticket {ticket_id} escalated successfully.")

def view_all_tickets(tickets):
    """Show a summary of all tickets"""

    print("\n=== All Tickets ===")

    for t in tickets.values():
        print(f"{t['ID']} | {t['Title']} | {t['Status']} | {t['Assignee']} | {t['Severity']}")


def main_menu():
    """Main menu navigation for the user"""
    while True:
        print("\n=== Helpdesk Main Menu ===")
        print("1. Submit New Ticket")
        print("2. Edit Ticket")
        print("3. Comment on Ticket")
        print("4. Close Ticket")
        print("5. Escalate Ticket")
        print("6. View All Tickets")
        print("7. Quit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_ticket()
        elif choice == "2":
            update_ticket(tickets)
        elif choice == "3":
            add_comment(tickets)
        elif choice == "4":
            close_ticket(tickets)
        elif choice == "5":
            escalate_ticket(tickets)
        elif choice == "6":
            view_all_tickets(tickets)
        elif choice == "7":
            confirm = input("Are you sure you want to quit? (yes/no): ").strip().lower()
            if confirm == "yes":
                print("Goodbye!")  
                # CS - confirms before exiting to prevent accidental closure
                break
        else:
            print("Invalid choice, please select again.")  


if __name__ == "__main__":
    main_menu()  