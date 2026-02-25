from helpdesk import tickets, add_ticket  # importing ticket data and add ticket function

# SHOW MENU FUNCTION
def show_menu():
    """Display main options to the user"""  # print menu title
    print("\nHelp Desk Menu")  # SDE - separates UI from logic
    print("1. List all tickets")  # CS - safe as no sensitive info shown
    print("2. Add a new ticket")  # AI - allows AI assisted categorisation
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

# MAIN MENU LOOP
def main_menu():
    """Run the menu until the user chooses to exit"""
    while True:
        show_menu()
        choice = input("Select an option (1-3): ").strip()  # CS - cleaned input avoids errors

        if choice == "1":
            list_tickets()
        elif choice == "2":
            add_ticket()
        elif choice == "3":
            # exit confirmation
            confirm = input("Are you sure you want to exit? (y/n): ").lower()
            if confirm == "y":
                print("Exiting the application. Bye!")
                break
            else:
                print("Returning to main menu...") 
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

            # SDE - keeps loop readable and maintainable
            # CS - input validation prevents crashes
            # AI - add_ticket predicts category automatically

# START THE APP
if __name__ == "__main__":  # only run below if executed directly
    main_menu()  # start the main menu for user interaction

    # SDE - separates function definitions from execution for testing
    # CS - prevents accidental execution when imported
    # AI - allows AI helper functions to be imported safely