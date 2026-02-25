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

# DELETE TICKET
def delete_ticket(tickets):
    """Delete a ticket by ID after confirmation"""
    
    # 1. Ask for Ticket ID
    ticket_id = input("Enter the Ticket ID to delete: ").strip()
    # SDE - input stored in variable, keeps logic clean
    # CS - .strip() prevents accidental spaces or injection

    # 2. Validate ID is numeric
    if not ticket_id.isdigit():
        print("Invalid Ticket ID. Must be numeric.")
        return
    # SDE - early exit for invalid inputs
    # CS - prevents errors from bad inputs

    # 3. Look for ticket in datastore
    found_ticket = tickets.get(ticket_id)
    if not found_ticket:
        print("Ticket not found. Please try again.")
        return
    # SDE - safe lookup using dictionary
    # CS - avoids showing wrong or sensitive info

    # AI enhancement - warn if high severity
    if found_ticket['Severity'].lower() == "high":
        print(" Warning: This is a HIGH severity ticket. Be careful before deleting!")

    # 4. Confirm deletion with user
    confirm = input(f"Are you sure you want to delete ticket '{found_ticket['Title']}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return
    # SDE - confirmation prevents accidental deletion
    # CS - prevents data loss from wrong inputs

    # 5. Delete ticket and save
    del tickets[ticket_id]  # remove from dict
    save_tickets(tickets)   # write updated data back to CSV
    print(f"Ticket {ticket_id} deleted successfully.")
    # SDE - separates deletion from saving
    # CS - ensures persistent deletion is safe and controlled

    # return deleted ticket for logging 
    return found_ticket

# UPDATE TICKET WITH VALIDATION AND LOGGING
def update_ticket(tickets):
    """Amend an existing ticket safely with validation, logging and AI suggestions."""

    # 1. Ask for Ticket ID
    ticket_id = input("Enter the Ticket ID to update: ").strip()
    # SDE - user input separated from logic
    # CS - ensure numeric input to prevent errors or injection

    # 2. Validate format
    if not ticket_id.isdigit():
        print("Invalid Ticket ID. Must be numeric.")
        return

    # 3. Check ticket exists
    ticket = tickets.get(ticket_id)
    if not ticket:
        print("Ticket not found.")
        return

    # 3a. Prevent updates if ticket is closed
    if ticket["Status"].lower() == "closed":
        print("Cannot update a closed ticket.")
        # SDE - following business rules
        # CS - prevents unauthorised changes to finalised records
        return

    # 4. Display current ticket details
    print("\nCurrent Ticket Details:")
    for key, value in ticket.items():
        print(f"{key}: {value}")

    # 5. Ask user which field to update
    field = input(
        "\nEnter the field you want to update "
        "(Title, Description, Assignee, Severity, Status, Category): "
    ).strip().title()

    # Prevent updating primary key
    if field == "ID":
        print("Primary key cannot be modified.")
        return

    if field not in ticket:
        print("Invalid field selected.")
        return

    # 6. Ask user for new value
    new_value = input(f"Enter new value for {field}: ").strip()
    if new_value == "":
        print("Field cannot be empty.")
        return
    # SDE - validate before changing internal data
    # CS - prevents corrupt or empty data

    # Validation
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

    # AI FEATURE
    if field == "Description":
        if "password" in new_value.lower() or "breach" in new_value.lower():
            print("AI Alert: This update may involve sensitive security information.")
            # AI - flag sensitive keywords for human attention
    if field == "Severity" and new_value.lower() == "high":
        print("AI Suggestion: Consider escalating this ticket to senior support.")
        # AI - recommend escalation based on severity

    # 7. Apply update
    old_value = ticket[field]
    ticket[field] = new_value
    # SDE - clearly track changes before applying

    # 8. Save changes
    save_tickets(tickets)

    # 9. Log entry
    from datetime import datetime
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ticket {ticket_id}: Field '{field}' updated from '{old_value}' to '{new_value}'\n"
    with open("logs/audit.log", "a", encoding="utf-8") as f:
        f.write(log_entry)
        # SDE - separate logging keeps code maintainable
        # CS - tracks changes for accountability

    print("Ticket updated successfully. Changes recorded in the log.")

    return ticket