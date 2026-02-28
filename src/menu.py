import os
from datetime import datetime
from helpdesk import tickets, view_ticket_details, update_ticket, delete_ticket  # importing existing helpdesk functions
import openai  # using OpenAI to suggest ticket categories

# SET UP OPENAI
# getting the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# warning if the key isn’t set
if not openai.api_key:
    print("Warning: OPENAI_API_KEY not set. AI suggestions will default to 'Software' category.")

# defining available categories
CATEGORIES = ["Hardware", "Software", "Network", "Security"]


# AI CATEGORY SUGGESTION FUNCTION
def ai_suggest_category(title, description):
    """
    Getting AI suggestion for ticket category based on title and description.
    Returning one of the predefined categories.
    """
    if not openai.api_key:
        # returning default if no key
        return "Software"

    # creating a prompt to send to OpenAI
    prompt = f"""
    Suggest the most appropriate category for a helpdesk ticket.
    Options: {CATEGORIES}
    Title: {title}
    Description: {description}
    Reply with only the category name.
    """

    try:
        # sending the request to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        # getting the AI's suggested category
        category = response.choices[0].message.content.strip()

        # returning default if suggestion is unexpected
        if category not in CATEGORIES:
            return "Software"

        return category

    except Exception as e:
        # returning default if API call fails
        print(f"AI suggestion failed: {e}")
        return "Software"


# ADD A NEW TICKET USING AI
def add_ticket_ai():
    """
    Getting ticket info from user, getting AI suggestion, allowing override, saving ticket.
    """
    # getting ticket title and description
    title = input("Enter ticket title: ").strip()
    description = input("Enter ticket description: ").strip()

    # getting AI suggested category
    suggested_category = ai_suggest_category(title, description)
    print(f"AI suggests category: {suggested_category}")

    # getting user override or accepting AI suggestion
    category = input(f"Enter category or press Enter to accept [{suggested_category}]: ").strip()
    if not category:
        category = suggested_category

    # getting new unique ticket ID
    new_id = max(tickets.keys()) + 1 if tickets else 100

    # saving ticket in dictionary
    tickets[new_id] = {
        "ID": new_id,
        "Title": title,
        "Description": description,
        "Assignee": "",
        "Severity": "Low",
        "Status": "Open",
        "Category": category,
        "Submission DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Comments": []
    }

    # confirming ticket saved
    print(f"Ticket {new_id} added successfully!")


# SHOW MENU
def show_menu():
    """Showing main menu options"""
    print("\nHelp Desk Menu")
    print("1. List all tickets")
    print("2. View ticket details")
    print("3. Add a new ticket")
    print("4. Update a ticket")
    print("5. Delete a ticket")
    print("6. Exit")


# LIST TICKETS
def list_tickets():
    """Listing all tickets"""
    if not tickets:
        print("No tickets are available.")
        return

    for t in tickets.values():
        print(f"{t['ID']}: {t['Title']} ({t['Category']}) - {t['Status']}")


# MAIN MENU LOOP
def main_menu():
    """Showing menu repeatedly until exit"""
    while True:
        show_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            list_tickets()
        elif choice == "2":
            view_ticket_details(tickets)
        elif choice == "3":
            add_ticket_ai()
        elif choice == "4":
            update_ticket(tickets)
        elif choice == "5":
            delete_ticket(tickets)
        elif choice == "6":
            confirm = input("Are you sure you want to exit? (y/n): ").lower()
            if confirm == "y":
                print("Exiting the application. Bye!")
                break
            else:
                print("Returning to main menu...")
        else:
            print("Invalid input. Please enter a number from 1 to 6.")


# START THE APP
if __name__ == "__main__":
    main_menu()