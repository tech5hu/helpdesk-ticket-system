from helpdesk import tickets, add_ticket # importing ticket data and add ticket function

# SHOW MENU FUNCTION
def show_menu():
    """Display main options to the user""" # print menu title
    print("\nHelp Desk Menu") # SDE - separates UI from logic
    print("1. List all tickets") # CS - safe as no sensitive info shown
    print("2. Add a new ticket") # AI - allows AI assisted categorisation
    print("3. Exit")

# LIST TICKETS FUNCTION
def list_tickets():
    """Print all the tickets in memory"""
    if not tickets:  # SDE - avoids errors when no tickets exist
        print("No tickets are available.")  # CS - safe, no sensitive info
        return

    for t in tickets.values():
        print(f"{t['ID']}: {t['Title']} ({t['Category']}) - {t['Status']}")
        # SDE - separates display logic from data storage
        # CS - avoids exposing raw file paths
        # AI - shows predicted AI category instantly