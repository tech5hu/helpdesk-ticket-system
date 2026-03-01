import os
import csv
from datetime import datetime
from helpdesk import delete_ticket 
import openai  # using OpenAI to suggest ticket categories and severity

# csv file path
CSV_FILE = "../data/helpdesk.csv"

# tickets dictionary (loaded from csv at startup)
tickets = {}

# set up OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# warning if the key isn’t set
if not openai.api_key:
    print("warning: OPENAI_API_KEY not set. ai suggestions will default to 'Software' category and 'Low' severity.")

# defining available categories and severities
CATEGORIES = ["Hardware", "Software", "Network", "Security"]
SEVERITIES = ["Low", "Medium", "High"]

# csv load + save functions
def load_tickets_from_csv():
    """loading tickets from csv at app start up"""
    global tickets
    if not os.path.exists(CSV_FILE):
        return
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                ticket_id = int(row["ID"])
            except ValueError:
                continue  # skip rows with invalid ID
            comments = eval(row["Comments"]) if row.get("Comments") else []
            submission_dt = row.get("Submission DateTime") or f"{row.get('Submission Date', '')} {row.get('Submission Time', '')}".strip()

            tickets[ticket_id] = {
                "ID": ticket_id,
                "Title": row["Title"],
                "Description": row["Description"],
                "Assignee": row.get("Assignee", ""),
                "Severity": row.get("Severity", "Low"),
                "Status": row.get("Status", "Open"),
                "Category": row.get("Category", "Software"),
                "Submission DateTime": submission_dt,
                "Comments": comments
            }

def save_tickets_to_csv():
    """saving tickets dictionary to csv file"""
    with open(CSV_FILE, "w", newline="") as f:
        fieldnames = ["ID", "Title", "Description", "Assignee", "Severity", "Status", "Category", "Submission DateTime", "Comments"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in tickets.values():
            row = t.copy()
            row["Comments"] = str(row.get("Comments", []))
            writer.writerow(row)
    print("tickets saved to csv.")

# ai category and severity function
def ai_suggest_category_severity(title, description):
    """getting ai suggestion for ticket category and severity, suppressing errors"""
    if not openai.api_key:
        return "Software", "Low"
    prompt = f"""
    suggest the most appropriate category and severity for a helpdesk ticket.
    categories: {CATEGORIES}
    severities: {SEVERITIES}
    title: {title}
    description: {description}
    reply with only the category and severity, separated by a comma.
    example: Software, High
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        result = response.choices[0].message.content.strip()
        parts = [p.strip() for p in result.split(",")]
        category = parts[0] if parts and parts[0] in CATEGORIES else "Software"
        severity = parts[1] if len(parts) > 1 and parts[1] in SEVERITIES else "Low"
        return category, severity
    except Exception:
        # silently suppress AI errors
        return "Software", "Low"

# add ticket function
def add_ticket_ai():
    """getting ticket info from user, getting ai suggestions, saving ticket and csv"""
    title = input("enter ticket title: ").strip()
    description = input("enter ticket description: ").strip()
    suggested_category, suggested_severity = ai_suggest_category_severity(title, description)
    print(f"ai suggests category: {suggested_category}, severity: {suggested_severity}")
    category = input(f"enter category or press enter to accept [{suggested_category}]: ").strip() or suggested_category
    severity = input(f"enter severity or press enter to accept [{suggested_severity}]: ").strip() or suggested_severity
    assignee = input("enter assignee (optional): ").strip()
    new_id = max(tickets.keys()) + 1 if tickets else 100
    tickets[new_id] = {
        "ID": new_id,
        "Title": title,
        "Description": description,
        "Assignee": assignee,
        "Severity": severity,
        "Status": "Open",
        "Category": category,
        "Submission DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Comments": []
    }
    save_tickets_to_csv()
    print(f"ticket {new_id} added successfully!")

# update ticket function
def update_ticket_ai(tickets):
    """updating ticket info, using ai suggestions, saving csv"""
    try:
        ticket_id = int(input("enter ticket id to update: ").strip())
    except ValueError:
        print("please enter a valid number")
        return
    if ticket_id in tickets:
        title = input("enter new title (leave blank to keep current): ").strip() or tickets[ticket_id]["Title"]
        description = input("enter new description (leave blank to keep current): ").strip() or tickets[ticket_id]["Description"]
        suggested_category, suggested_severity = ai_suggest_category_severity(title, description)
        print(f"ai suggests category: {suggested_category}, severity: {suggested_severity}")
        category = input(f"enter category or press enter to accept [{suggested_category}]: ").strip() or suggested_category
        severity = input(f"enter severity or press enter to accept [{suggested_severity}]: ").strip() or suggested_severity
        assignee = input(f"enter assignee or press enter to keep current [{tickets[ticket_id]['Assignee']}]: ").strip() or tickets[ticket_id]['Assignee']
        tickets[ticket_id].update({"Title": title, "Description": description, "Category": category, "Severity": severity, "Assignee": assignee})
        save_tickets_to_csv()
        print(f"ticket {ticket_id} updated successfully!")
    else:
        print("ticket id not found.")

# close ticket function
def close_ticket(tickets):
    """closing a ticket by setting status to closed and saving csv"""
    try:
        ticket_id = int(input("enter ticket id to close: ").strip())
    except ValueError:
        print("please enter a valid number")
        return
    if ticket_id in tickets:
        tickets[ticket_id]['Status'] = 'Closed'
        save_tickets_to_csv()
        print(f"ticket {ticket_id} closed.")
    else:
        print("ticket id not found.")

# escalate ticket function
def escalate_ticket_ai(tickets):
    """escalating ticket severity using ai and saving csv"""
    try:
        ticket_id = int(input("enter ticket id to escalate: ").strip())
    except ValueError:
        print("please enter a valid number")
        return
    if ticket_id in tickets:
        title = tickets[ticket_id]["Title"]
        description = tickets[ticket_id]["Description"]
        _, suggested_severity = ai_suggest_category_severity(title, description)
        if suggested_severity == "High":
            tickets[ticket_id]['Severity'] = "High"
            save_tickets_to_csv()
            print(f"ticket {ticket_id} escalated to high severity by ai.")
        else:
            print(f"ticket {ticket_id} severity unchanged (ai suggested: {suggested_severity}).")
    else:
        print("ticket id not found.")

# add comment function
def comment_ticket(tickets):
    """adding a comment to a ticket and saving csv"""
    try:
        ticket_id = int(input("enter ticket id to comment on: ").strip())
    except ValueError:
        print("please enter a valid number")
        return
    if ticket_id in tickets:
        author = input("enter your name: ").strip()
        comment = input("enter comment: ").strip()
        now = datetime.now()
        tickets[ticket_id]['Comments'].append({
            "Author": author,
            "Date": now.strftime("%Y-%m-%d"),
            "Time": now.strftime("%H:%M:%S"),
            "Content": comment
        })
        save_tickets_to_csv()
        print(f"comment added to ticket {ticket_id}.")
    else:
        print("ticket id not found.")

# delete ticket function (fixed type conversion)
def delete_ticket_with_input(tickets):
    """deleting a ticket and saving csv"""
    try:
        ticket_id = int(input("enter ticket id to delete: ").strip())
    except ValueError:
        print("please enter a valid number")
        return
    if ticket_id in tickets:
        del tickets[ticket_id]
        save_tickets_to_csv()
        print(f"ticket {ticket_id} deleted successfully!")
    else:
        print("ticket id not found.")

# auto escalate function
def auto_escalate_high_severity():
    """automatically escalate any open high severity tickets"""
    for t in tickets.values():
        if t['Severity'] == "High" and t['Status'] != "Closed":
            print(f"ticket {t['ID']} is high severity and open! automatically suggesting escalation.")

# menu display + loop
def show_menu():
    """showing main menu options"""
    print("\nhelp desk menu")
    print("1. list all tickets")
    print("2. view ticket details")
    print("3. add a new ticket")
    print("4. update a ticket")
    print("5. delete a ticket")
    print("6. close a ticket")
    print("7. escalate a ticket")
    print("8. comment on a ticket")
    print("9. exit")

# list all tickets
def list_tickets():
    """listing all tickets and auto-suggesting escalation"""
    if not tickets:
        print("no tickets are available.")
        return
    for t in tickets.values():
        print(f"{t['ID']}: {t['Title']} ({t['Category']}) - {t['Status']}, severity: {t['Severity']}")
    auto_escalate_high_severity()

# view full ticket details
def view_ticket_details_with_alerts(ticket_dict):
    """viewing ticket details with comments and auto-suggesting escalation"""
    try:
        ticket_id = int(input("enter ticket id to view: ").strip())
    except ValueError:
        print("please enter a valid number")
        return
    if ticket_id in ticket_dict:
        t = ticket_dict[ticket_id]
        print(f"\n--- ticket {ticket_id} details ---")
        print(f"title       : {t['Title']}")
        print(f"description : {t['Description']}")
        print(f"category    : {t['Category']}")
        print(f"severity    : {t['Severity']}")
        print(f"status      : {t['Status']}")
        print(f"assignee    : {t['Assignee']}")
        print(f"submitted   : {t['Submission DateTime']}")
        if t['Comments']:
            print("comments    :")
            for c in t['Comments']:
                print(f"  - [{c['Date']} {c['Time']}] {c['Author']}: {c['Content']}")
        else:
            print("comments    : none")
    else:
        print("ticket not found.")
    auto_escalate_high_severity()

def main_menu():
    """showing menu repeatedly until exit"""
    load_tickets_from_csv()  # load tickets at startup
    while True:
        show_menu()
        choice = input("select an option (1-9): ").strip()
        if choice == "1":
            list_tickets()
        elif choice == "2":
            view_ticket_details_with_alerts(tickets)
        elif choice == "3":
            add_ticket_ai()
        elif choice == "4":
            update_ticket_ai(tickets)
        elif choice == "5":
            delete_ticket_with_input(tickets)
        elif choice == "6":
            close_ticket(tickets)
        elif choice == "7":
            escalate_ticket_ai(tickets)
        elif choice == "8":
            comment_ticket(tickets)
        elif choice == "9":
            confirm = input("are you sure you want to exit? (y/n): ").lower()
            if confirm == "y":
                print("exiting the application. bye!")
                break
            else:
                print("returning to main menu...")
        else:
            print("invalid input. please enter a number from 1 to 9.")

# start the app
if __name__ == "__main__":
    main_menu()