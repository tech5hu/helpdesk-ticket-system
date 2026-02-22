from helpdesk import tickets, add_ticket # importing ticket data and add ticket function

# SHOW MENU FUNCTION
def show_menu():
    """Display main options to the user""" # print menu title
    print("\nHelp Desk Menu") # SDE - separates UI from logic
    print("1. List all tickets") # CS - safe as no sensitive info shown
    print("2. Add a new ticket") # AI - allows AI assisted categorisation
    print("3. Exit")