# Import the Flask web framework and helper functions
from flask import Flask, render_template, request  # render_template displays HTML pages, request gets the form input
from helpdesk import tickets, save_tickets  # existing helpdesk ticket data and the save function

# Creating a new web app
app = Flask(__name__)  # Telling Flask where to look for files

# Home page route - shows all tickets
@app.route("/")  # when the user goes to http://localhost:5000/
def index():
    # Display all tickets on the homepage
    # tickets.values() gives all the tickets as a list
    return render_template("index.html", tickets=tickets.values())

# Page to add a new ticket
@app.route("/add", methods=["GET", "POST"])  # allows showing user the form and submitting it
def add_ticket_web():
    if request.method == "POST":  # if user has submitted the form
        # Get the data the user typed into the form
        title = request.form["title"]
        description = request.form["description"]
        assignee = request.form["assignee"]
        severity = request.form["severity"]
        status = request.form["status"]

        # Automatically assign a new unique ticket ID
        ticket_id = str(max(map(int, tickets.keys()), default=100) + 1)

        # Create a new ticket in memory
        tickets[ticket_id] = {
            "ID": ticket_id,
            "Title": title,
            "Description": description,
            "Assignee": assignee,
            "Severity": severity,
            "Status": status,
            "Category": "Software",  
            "Submission Date": "25/02/2026",  
            "Submission Time": "19:30:10"  
        }

        # Saving the ticket to the CSV file so it isn't lost
        save_tickets(tickets)

        # Letting user know the ticket was added successfully
        return "Ticket added!"

    # If user just opens the page, show the form
    return render_template("add.html")

# Page to view all tickets in detail
@app.route("/view")
def view_tickets_web():
    # Show all tickets using the view.html template
    return render_template("view.html", tickets=tickets.values())

# Page to update an existing ticket
@app.route("/update/<ticket_id>", methods=["GET", "POST"])
def update_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)  # get ticket by ID
    if not ticket:  # if ticket doesn't exist
        return f"Ticket {ticket_id} not found."

    if request.method == "POST":  # if form submitted
        # Update ticket info from form data
        ticket["Title"] = request.form["title"]
        ticket["Description"] = request.form["description"]
        ticket["Assignee"] = request.form["assignee"]
        ticket["Severity"] = request.form["severity"]
        ticket["Status"] = request.form["status"]
        ticket["Category"] = request.form["category"]

        # Save updated tickets
        save_tickets(tickets)
        return f"Ticket {ticket_id} updated successfully!"

    # Show form pre filled with current ticket data
    return render_template("update.html", ticket=ticket)

# Page to delete a ticket
@app.route("/delete/<ticket_id>", methods=["GET", "POST"])
def delete_ticket_web(ticket_id):
    ticket = tickets.get(ticket_id)  # get ticket by ID
    if not ticket:  # if ticket doesn't exist
        return f"Ticket {ticket_id} not found."

    if request.method == "POST":  # if form submitted
        confirm = request.form.get("confirm")  # check confirmation
        if confirm == "yes":
            tickets.pop(ticket_id)  # remove ticket
            save_tickets(tickets)  # save changes
            return f"Ticket {ticket_id} deleted successfully!"
        else:
            return "Deletion cancelled."

    # Show confirmation page before deleting
    return render_template("delete.html", ticket=ticket)

# Run the app if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)  # debug=True shows errors while developing