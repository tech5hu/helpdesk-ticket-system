from helpdesk import tickets, add_ticket, view_ticket_details, update_ticket, delete_ticket  # importing ticket data and functions

# SHOW MENU FUNCTION
def show_menu():
    """Display main options to the user"""  # print menu title
    print("\nHelp Desk Menu")  # SDE - separates UI from logic
    print("1. List all tickets")  # CS - safe as no sensitive info shown
    print("2. View ticket details")  # access to full ticket info
    print("3. Add a new ticket")  # AI - allows assisted categorisation
    print("4. Update a ticket")  # SDE - safely update ticket data
    print("5. Delete a ticket")  # CS - confirmation prevents accidental deletion
    print("6. Exit")  # SDE - exit confirmation implemented

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
        choice = input("Select an option (1-6): ").strip()  # CS - cleaned input avoids errors

        if choice == "1":
            list_tickets()  # SDE - separate function keeps code organised
        elif choice == "2":
            view_ticket_details(tickets)  # SDE - separate logic for viewing
            # CS - safe lookup, prevents errors or data leaks
            # AI - high severity alerts are shown automatically
        elif choice == "3":
            add_ticket()  # SDE - separate function, modular design
            # CS - input validation inside function
            # AI - predicts category automatically
        elif choice == "4":
            update_ticket(tickets)  # SDE - separate logic, easier maintenance
            # CS - validation prevents bad data
            # AI - warns about sensitive keywords or high severity
        elif choice == "5":
            delete_ticket(tickets)  # SDE - separate function, clean deletion process
            # CS - confirmation prevents accidental deletion
            # AI - warns if high severity ticket
        elif choice == "6":
            confirm = input("Are you sure you want to exit? (y/n): ").lower()  # CS - prevents accidental exit
            if confirm == "y":
                print("Exiting the application. Bye!")
                break  # SDE - clean exit from main loop
            else:
                print("Returning to main menu...") 
        else:
            print("Invalid input. Please enter a number from 1 to 6.")

# START THE APP
if __name__ == "__main__":  # only run below if executed directly
    main_menu()  # start the main menu for user interaction
    # SDE - separates function definitions from execution for testing
    # CS - prevents accidental execution when imported
    # AI - allows AI helper functions to be imported safely